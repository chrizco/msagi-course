# MSAGI RAG Pipeline Project Report

## Introduction

This project built a small Retrieval-Augmented Generation pipeline for searching across multiple PDF documents. The goal was to load PDF files, split them into smaller chunks, convert those chunks into embeddings, store them in a FAISS vectorstore, and retrieve relevant chunks for a user question.

RAG is useful because it allows a system to search external documents and retrieve relevant context instead of relying only on a model's internal knowledge.

## Implementation Overview

The pipeline used three PDF documents as the input dataset. The PDFs were loaded with LangChain's PyPDFLoader and split into smaller text chunks with RecursiveCharacterTextSplitter.

The chunks were embedded using the OpenAI embedding model text-embedding-3-small. The resulting vectors were stored in a FAISS vectorstore. A sample query was then used to retrieve relevant chunks with semantic similarity search.

## Metrics

- Number of PDFs: 3
- Total loaded pages: 37
- Total chunks: 205
- Average chunk size: 908 characters
- Embedding model: text-embedding-3-small
- Vectorstore: FAISS

## Sample Query

Query:

What does the document say about BPC-157 and wound healing?

Best retrieved result:

- Source: PMID-25995620_Huang_2015_Body-protective-compound-157-enhances-alkali-burned-wound-healing.pdf
- Page: 12

Preview:

bFGF- or BPC-157-treated groups was better than that in  the model control group. These data also suggest that the  effect of BPC-157 on alkali-burn wound repair is, apparently,  comparable with that of bFGF. More interestingly, BPC- 157 is highly stable and resistant to hydrolysis or enzyme  digestion, even in the gastric juice. Furthermore, it is easily  dissolved in water and needs no carrier for its application.13  These findings indicate that BPC-157 may become a thera- peutic agent for the treatment of chemical-induced burn  wound. Previous studies have demonstrated that BPC-157  promotes the healing of different tissues, including skin, 36  muscle,15,37–39 bone, 40 ligament, 41 and tendon 42 in various  animal models. However, the underlying mechanism has  not been fully elucidated. The theory of cell biology in wound healing emphasized  that endothelial cells, fibroblasts, and keratinocytes may  contribute to the proliferation stage in the wound healing

## Issues Faced

One issue was that the notebook initially searched for PDFs in the wrong folder because VS Code/Jupyter executed the notebook from the notebooks directory. This was fixed by setting the project root to one folder above the notebook folder.

Another issue was that the .env file was not properly saved at first, so the notebook still loaded the placeholder OpenAI API key. Reloading the VS Code window and confirming that the API key loaded correctly solved the problem.

A retrieval quality issue also appeared when an earlier query returned mainly source or reference-like chunks instead of useful content. This was improved by using a more specific query about BPC-157 and wound healing.

## Conclusion

The project successfully implemented a basic RAG pipeline using PDF loading, chunking, OpenAI embeddings, FAISS vector storage, and semantic retrieval. The system was able to retrieve relevant document chunks for a sample user question.

The project helped clarify the practical steps required to build a RAG pipeline: preparing source documents, splitting them into chunks, embedding the chunks, storing them in a vector database, and retrieving relevant results.

## Possible Improvements

Future improvements could include testing different chunk sizes and overlaps, comparing multiple retrieval queries, filtering out references or bibliography sections, adding a generated answer step with GPT, and improving the display of retrieved results with clearer source and page references.
