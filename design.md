# DRISHTI-AI System Design

## 1. Architecture Overview

DRISHTI-AI follows a voice-driven, Retrieval-Augmented Generation (RAG) architecture 
designed to deliver syllabus-aligned, accessible learning for visually impaired students.

The system uses a hybrid cloud architecture:
- CPU-based services handle API requests, retrieval logic, and session control.
- GPU-based services handle LLM inference for high-performance response generation.

The design ensures:
- Low latency
- High accuracy (syllabus grounding)
- Cloud scalability
- Accessibility-first interaction

## 2. High-Level System Components

### 2.1 Voice Input Module

- Captures real-time audio from the user.
- Supports microphone-based interaction.
- Sends audio stream to ASR service.
- Designed for hands-free, fully voice-based usage.


### 2.2 Automatic Speech Recognition (ASR)

- Converts speech input into text.
- Optimized for academic vocabulary and subject-specific terms.
- Handles pronunciation variations.
- Returns transcribed text to the backend API.

Example:
Voice: "Explain Newton's First Law"
Output: "Explain Newton's First Law"


### 2.3 Intent Classification (NLU Layer)

After transcription, Natural Language Understanding (NLU) classifies the input into:

1. Navigation Command  
2. Lecture Request  
3. Doubt Query  

Routing logic:
- Navigation → Syllabus Controller
- Lecture → Audio Content Module
- Doubt → RAG Pipeline

This ensures modular processing and clean separation of concerns.


### 2.4 Syllabus Content Management

Syllabus is structured hierarchically:

Class → Subject → Chapter → Topic

Content preprocessing includes:
- Chunking syllabus into semantic units
- Generating embeddings
- Storing embeddings in vector database

This allows precise chapter-level retrieval.

### 2.5 RAG Pipeline (Doubt Resolution Engine)

The RAG architecture ensures accurate and syllabus-grounded answers.

#### Step 1: Query Normalization
- Extract core meaning of question
- Remove unnecessary variations
- Add contextual information (current class, subject, chapter)

#### Step 2: Embedding Generation
- Convert query into vector representation using Sentence Transformers

#### Step 3: Semantic Retrieval
- Perform similarity search in FAISS vector database
- Retrieve top-k relevant syllabus chunks

#### Step 4: Context Augmentation
- Combine retrieved chunks into structured context
- Prepare fixed prompt template

#### Step 5: LLM Inference
- LLM (LLaMA / DeepSeek) generates answer strictly from retrieved content
- Hallucination minimized through prompt constraints

#### Step 6: Response Validation
- Ensure output aligns with retrieved content
- Optional confidence scoring (future enhancement)


### 2.6 Text-to-Speech (TTS) Output

- Converts generated answer into natural audio.
- Ensures proper pacing and pronunciation.
- Supports pause, resume, replay functionality.
- Designed for clarity in formulas and scientific explanations.

Final Output:
Clear, accessible audio response delivered to the user.

## 3. End-to-End Data Flow

1. User speaks query
2. Voice captured via frontend
3. ASR converts speech to text
4. Backend receives transcribed text
5. Intent classification determines route
6. If doubt:
   - Query embedding generated
   - Semantic retrieval from vector DB
   - Context passed to LLM
   - Answer generated
7. TTS converts text to speech
8. Audio response streamed back to user

Flow Summary:
Voice → STT → Intent Detection → Retrieval → LLM → TTS → Audio Output


## 4. Cloud Deployment Architecture

### 4.1 Backend Layer

- FastAPI handles API requests
- Hosted on Google Cloud Run
- Stateless microservices design

Responsibilities:
- Request routing
- Session tracking
- Retrieval calls
- LLM API calls

### 4.2 LLM Inference Layer

- Deployed on GPU-enabled Virtual Machine or Vertex AI
- Handles heavy model inference
- Separated from backend for scalability

### 4.3 Vector Database Layer

- FAISS for high-speed similarity search
- Stores syllabus embeddings
- Optimized for fast retrieval

### 4.4 Speech Services

- Google Speech-to-Text for ASR
- Google Text-to-Speech for output

### 4.5 Session Management

- Redis used for:
  - Maintaining user session
  - Tracking current class/chapter
  - Managing navigation state

## 5. Scalability Strategy

### 5.1 Microservices Architecture

Each major module operates independently:
- ASR service
- Retrieval service
- LLM inference service
- TTS service

This allows horizontal scaling.

### 5.2 Auto Scaling

- Cloud Run automatically scales based on request load.
- GPU VM scaling based on inference demand.

### 5.3 Data Expansion

- New classes or boards can be added by:
  - Ingesting syllabus
  - Generating embeddings
  - Updating vector database

No architecture changes required.

### 5.4 Multi-language Expansion (Future)

- Add multilingual embeddings
- Integrate regional ASR models
- Expand TTS voice models

## 6. Security & Reliability Design

- Secure API endpoints with authentication
- HTTPS communication
- Logging and monitoring
- Graceful failure handling
- Error fallback messages

## 7. Design Principles

1. Accessibility First
2. Syllabus Grounded AI
3. Modular & Scalable
4. Low Latency
5. Minimal Hallucination

## 8. Future Enhancements

- Offline content caching
- Voice-based assessment module
- Teacher analytics dashboard
- Personalized adaptive learning engine
