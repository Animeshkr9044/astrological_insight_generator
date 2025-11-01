#!/bin/bash

# Query Script for Astrological Insight Generator
# Convenient command-line interface to query the API

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default values
API_URL="${API_URL:-http://localhost:8000}"
NAME=""
BIRTH_DATE=""
BIRTH_TIME=""
BIRTH_PLACE=""
LANGUAGE="en"

# Functions
print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Astrological Insight Generator - Query Tool           ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_usage() {
    echo "Usage: ./query.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --name NAME          User's name (required)"
    echo "  --date DATE          Birth date in YYYY-MM-DD format (required)"
    echo "  --time TIME          Birth time in HH:MM format (required)"
    echo "  --place PLACE        Birth place (required)"
    echo "  --language LANG      Language (en or hi, default: en)"
    echo "  --url URL            API URL (default: http://localhost:8000)"
    echo "  --health             Check API health"
    echo "  --zodiac DATE        Get zodiac info only for a date"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./query.sh --name \"Ritika\" --date \"1995-08-20\" --time \"14:30\" --place \"Jaipur, India\""
    echo "  ./query.sh --name \"John\" --date \"1990-03-15\" --time \"09:00\" --place \"New York, USA\" --language en"
    echo "  ./query.sh --health"
    echo "  ./query.sh --zodiac \"1995-08-20\""
}

# Health check
check_health() {
    print_header
    echo -e "${YELLOW}Checking API health...${NC}"
    echo ""
    
    response=$(curl -s "${API_URL}/api/v1/health")
    
    if [ $? -eq 0 ]; then
        echo "$response" | python3 -m json.tool
        echo ""
        echo -e "${GREEN}✅ API is healthy${NC}"
    else
        echo -e "${RED}❌ Failed to connect to API at ${API_URL}${NC}"
        exit 1
    fi
}

# Get zodiac info only
get_zodiac_info() {
    local date=$1
    print_header
    echo -e "${YELLOW}Getting zodiac information for ${date}...${NC}"
    echo ""
    
    response=$(curl -s -X POST "${API_URL}/api/v1/zodiac" \
        -H "Content-Type: application/json" \
        -d "{\"birth_date\": \"${date}\"}")
    
    if [ $? -eq 0 ]; then
        echo "$response" | python3 -m json.tool
        echo ""
        echo -e "${GREEN}✅ Zodiac info retrieved${NC}"
    else
        echo -e "${RED}❌ Failed to get zodiac info${NC}"
        exit 1
    fi
}

# Generate insight
generate_insight() {
    print_header
    echo -e "${YELLOW}Generating insight for ${NAME}...${NC}"
    echo ""
    
    request_json=$(cat <<EOF
{
    "name": "${NAME}",
    "birth_date": "${BIRTH_DATE}",
    "birth_time": "${BIRTH_TIME}",
    "birth_place": "${BIRTH_PLACE}",
    "language": "${LANGUAGE}"
}
EOF
)
    
    echo -e "${BLUE}Request:${NC}"
    echo "$request_json" | python3 -m json.tool
    echo ""
    echo -e "${YELLOW}Sending request to ${API_URL}/api/v1/insight...${NC}"
    echo ""
    
    response=$(curl -s -X POST "${API_URL}/api/v1/insight" \
        -H "Content-Type: application/json" \
        -d "$request_json")
    
    if [ $? -eq 0 ]; then
        echo -e "${BLUE}Response:${NC}"
        echo "$response" | python3 -m json.tool
        echo ""
        
        # Extract and display insight nicely
        zodiac=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('zodiac', ''))")
        insight=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('insight', ''))")
        
        if [ -n "$zodiac" ] && [ -n "$insight" ]; then
            echo ""
            echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║  Zodiac: ${zodiac}${NC}"
            echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
            echo ""
            echo -e "${BLUE}${insight}${NC}"
            echo ""
            echo -e "${GREEN}✅ Insight generated successfully${NC}"
        fi
    else
        echo -e "${RED}❌ Failed to generate insight${NC}"
        exit 1
    fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --name)
            NAME="$2"
            shift 2
            ;;
        --date)
            BIRTH_DATE="$2"
            shift 2
            ;;
        --time)
            BIRTH_TIME="$2"
            shift 2
            ;;
        --place)
            BIRTH_PLACE="$2"
            shift 2
            ;;
        --language)
            LANGUAGE="$2"
            shift 2
            ;;
        --url)
            API_URL="$2"
            shift 2
            ;;
        --health)
            check_health
            exit 0
            ;;
        --zodiac)
            get_zodiac_info "$2"
            exit 0
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo ""
            print_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$NAME" ] || [ -z "$BIRTH_DATE" ] || [ -z "$BIRTH_TIME" ] || [ -z "$BIRTH_PLACE" ]; then
    echo "Error: Missing required parameters"
    echo ""
    print_usage
    exit 1
fi

# Generate insight
generate_insight

