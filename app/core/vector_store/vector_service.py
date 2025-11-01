"""
Vector store service for semantic retrieval of astrological knowledge.

Uses Qdrant for vector storage and sentence-transformers for embeddings.
"""
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Service for managing and querying astrological knowledge using vector embeddings.
    
    Supports both in-memory and server-based Qdrant instances.
    """
    
    def __init__(
        self,
        enabled: bool = True,
        mode: str = "memory",
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None,
        embedding_model: str = "all-MiniLM-L6-v2",
        collection_name: str = "astrological_knowledge",
    ):
        """
        Initialize the vector store service.
        
        Args:
            enabled: Whether vector store is enabled
            mode: "memory" for in-memory or "server" for remote Qdrant
            qdrant_url: URL for Qdrant server (required if mode="server")
            qdrant_api_key: API key for Qdrant server
            embedding_model: Name of sentence-transformers model
            collection_name: Name of the vector collection
        """
        self.enabled = enabled
        self.mode = mode
        self.collection_name = collection_name
        self.client = None
        self.encoder = None
        self.initialized = False
        
        if not enabled:
            logger.info("Vector store is disabled")
            return
        
        try:
            # Import dependencies only if enabled
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams, PointStruct
            from sentence_transformers import SentenceTransformer
            
            # Store imports for later use
            self.Distance = Distance
            self.VectorParams = VectorParams
            self.PointStruct = PointStruct
            
            # Initialize embedding model
            logger.info(f"Loading embedding model: {embedding_model}")
            self.encoder = SentenceTransformer(embedding_model)
            self.vector_size = self.encoder.get_sentence_embedding_dimension()
            
            # Initialize Qdrant client
            if mode == "memory":
                logger.info("Initializing in-memory Qdrant client")
                self.client = QdrantClient(":memory:")
            elif mode == "server":
                if not qdrant_url:
                    raise ValueError("qdrant_url is required for server mode")
                logger.info(f"Connecting to Qdrant server: {qdrant_url}")
                self.client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key,
                )
            else:
                raise ValueError(f"Invalid mode: {mode}. Must be 'memory' or 'server'")
            
            self.initialized = True
            logger.info("Vector store service initialized successfully")
            
        except ImportError as e:
            logger.error(f"Failed to import required libraries: {e}")
            logger.error("Install with: pip install qdrant-client sentence-transformers")
            self.enabled = False
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            self.enabled = False
    
    def is_available(self) -> bool:
        """Check if vector store is available and ready."""
        return self.enabled and self.initialized and self.client is not None
    
    def _create_collection(self):
        """Create the vector collection if it doesn't exist."""
        if not self.is_available():
            return
        
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_exists = any(c.name == self.collection_name for c in collections)
            
            if not collection_exists:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=self.VectorParams(
                        size=self.vector_size,
                        distance=self.Distance.COSINE,
                    ),
                )
                logger.info(f"Collection '{self.collection_name}' created successfully")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
                
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise
    
    def load_corpus(self, corpus_path: Optional[str] = None) -> bool:
        """
        Load astrological corpus into the vector store.
        
        Args:
            corpus_path: Path to corpus JSON file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_available():
            logger.warning("Vector store not available, skipping corpus load")
            return False
        
        try:
            # Default corpus path
            if corpus_path is None:
                corpus_path = Path(__file__).parent.parent.parent / "data" / "astrological_corpus.json"
            else:
                corpus_path = Path(corpus_path)
            
            if not corpus_path.exists():
                logger.error(f"Corpus file not found: {corpus_path}")
                return False
            
            # Load corpus
            logger.info(f"Loading corpus from: {corpus_path}")
            with open(corpus_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            corpus_items = data.get("corpus", [])
            if not corpus_items:
                logger.warning("Empty corpus")
                return False
            
            # Create collection
            self._create_collection()
            
            # Check if collection already has data
            collection_info = self.client.get_collection(self.collection_name)
            if collection_info.points_count > 0:
                logger.info(f"Collection already has {collection_info.points_count} points, skipping load")
                return True
            
            # Prepare texts and metadata
            texts = [item["text"] for item in corpus_items]
            
            # Generate embeddings in batches
            logger.info(f"Generating embeddings for {len(texts)} documents...")
            embeddings = self.encoder.encode(
                texts,
                show_progress_bar=False,
                convert_to_numpy=True,
            )
            
            # Create points
            points = []
            for idx, (item, embedding) in enumerate(zip(corpus_items, embeddings)):
                point = self.PointStruct(
                    id=idx,
                    vector=embedding.tolist(),
                    payload={
                        "doc_id": item["id"],
                        "zodiac": item["zodiac"],
                        "category": item["category"],
                        "text": item["text"],
                    },
                )
                points.append(point)
            
            # Upload to Qdrant
            logger.info(f"Uploading {len(points)} points to Qdrant...")
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            
            logger.info(f"Successfully loaded {len(points)} documents into vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error loading corpus: {e}", exc_info=True)
            return False
    
    def search(
        self,
        query: str,
        zodiac: Optional[str] = None,
        top_k: int = 3,
        score_threshold: float = 0.5,
    ) -> List[Dict]:
        """
        Search for relevant astrological knowledge.
        
        Args:
            query: Search query
            zodiac: Filter by zodiac sign (optional)
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of relevant documents with scores
        """
        if not self.is_available():
            logger.warning("Vector store not available")
            return []
        
        try:
            # Generate query embedding
            query_vector = self.encoder.encode(query, convert_to_numpy=True).tolist()
            
            # Prepare filters
            query_filter = None
            if zodiac:
                from qdrant_client.models import Filter, FieldCondition, MatchValue
                
                # Search for exact zodiac match or general guidance
                query_filter = Filter(
                    should=[
                        FieldCondition(
                            key="zodiac",
                            match=MatchValue(value=zodiac),
                        ),
                    ]
                )
            
            # Search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=query_filter,
                score_threshold=score_threshold,
            )
            
            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "text": hit.payload["text"],
                    "zodiac": hit.payload["zodiac"],
                    "category": hit.payload["category"],
                    "score": hit.score,
                })
            
            logger.info(f"Found {len(results)} relevant documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}", exc_info=True)
            return []
    
    def get_context_for_insight(
        self,
        zodiac: str,
        name: str,
        birth_place: str,
        top_k: int = 3,
    ) -> str:
        """
        Get relevant context for generating an insight.
        
        Args:
            zodiac: User's zodiac sign
            name: User's name
            birth_place: User's birth place
            top_k: Number of context items to retrieve
            
        Returns:
            Formatted context string
        """
        if not self.is_available():
            return ""
        
        # Create search query
        query = f"Daily guidance and personality insights for {zodiac}"
        
        # Search for relevant context
        results = self.search(query=query, zodiac=zodiac, top_k=top_k)
        
        if not results:
            return ""
        
        # Format context
        context_parts = ["Relevant Astrological Knowledge:"]
        for i, result in enumerate(results, 1):
            context_parts.append(f"\n{i}. {result['text']}")
        
        return "\n".join(context_parts)
    
    def clear_collection(self):
        """Clear all data from the collection."""
        if not self.is_available():
            return
        
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' cleared")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")


# Singleton instance (cached)
@lru_cache(maxsize=1)
def get_vector_store_service(
    enabled: bool = True,
    mode: str = "memory",
    qdrant_url: Optional[str] = None,
    qdrant_api_key: Optional[str] = None,
    embedding_model: str = "all-MiniLM-L6-v2",
    collection_name: str = "astrological_knowledge",
) -> VectorStoreService:
    """
    Get or create a singleton vector store service instance.
    
    Returns:
        VectorStoreService instance
    """
    service = VectorStoreService(
        enabled=enabled,
        mode=mode,
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key,
        embedding_model=embedding_model,
        collection_name=collection_name,
    )
    
    # Auto-load corpus on initialization
    if service.is_available():
        service.load_corpus()
    
    return service

