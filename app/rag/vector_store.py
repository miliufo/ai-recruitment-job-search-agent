from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = PROJECT_ROOT / "data" / "chroma"

JOB_COLLECTION_NAME = "jobs"


def get_chroma_client() -> chromadb.PersistentClient:
    """
    Create a persistent ChromaDB client.

    Vector data is stored locally inside:
    data/chroma/
    """
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)

    return chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )


def get_job_collection() -> Collection:
    """
    Return the persistent collection used for job embeddings.
    """
    client = get_chroma_client()

    return client.get_or_create_collection(
        name=JOB_COLLECTION_NAME,
        metadata={
            "description": "Vector index for recruitment job postings"
        }
    )


def get_collection_stats() -> dict:
    """
    Return basic information about the job vector collection.
    """
    collection = get_job_collection()

    return {
        "collection_name": JOB_COLLECTION_NAME,
        "document_count": collection.count(),
        "storage_path": str(CHROMA_PATH),
    }


def reset_job_collection() -> Collection:
    """
    Delete and recreate the job collection.

    Useful when rebuilding the vector index.
    """
    client = get_chroma_client()

    try:
        client.delete_collection(JOB_COLLECTION_NAME)
    except Exception:
        pass

    return client.get_or_create_collection(
        name=JOB_COLLECTION_NAME,
        metadata={
            "description": "Vector index for recruitment job postings"
        }
    )