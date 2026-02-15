# DRISHTI-AI Requirements Document

## 1. Project Overview

DRISHTI-AI is a voice-first AI-powered learning platform designed specifically for visually impaired students. 
The system converts structured syllabus content into interactive audio lectures and provides real-time doubt resolution using Retrieval-Augmented Generation (RAG).

The platform aims to deliver independent, accessible, and syllabus-aligned education without reliance on visual interfaces.


## 2. Problem Context

Most digital education platforms are designed for sighted users and rely heavily on text, diagrams, and visual navigation. 

Visually impaired students face:
- High dependency on human assistance
- Limited access to structured syllabus content
- Difficulty understanding visual concepts in STEM subjects
- Lack of interactive doubt-solving tools

DRISHTI-AI addresses these gaps through a fully voice-driven system.


## 3. Functional Requirements

### 3.1 Voice Interaction

- The system must accept real-time voice input from users.
- The system must support natural language voice commands.
- The system must work without requiring any visual interaction.
- The system must support commands such as:
  - "Start Class 10 Chemistry Chapter 1"
  - "Pause lecture"
  - "Explain Newton's Laws"
  - "Go to next chapter"

### 3.2 Speech-to-Text (ASR)

- The system must convert speech to text using Automatic Speech Recognition (ASR).
- The ASR must be optimized for educational vocabulary.
- The system must handle minor pronunciation variations.

### 3.3 Intent Classification (NLU)

- The system must classify user input into:
  - Navigation commands
  - Lecture requests
  - Doubt queries
- The system must route the request to the correct module.


### 3.4 Syllabus Management

- The system must organize content hierarchically:
  Class → Subject → Chapter → Topic
- The system must retrieve content based on voice-based navigation.
- The system must support structured chapter-wise learning.


### 3.5 RAG-Based Doubt Resolution

- The system must implement Retrieval-Augmented Generation (RAG).
- The knowledge base must contain syllabus-approved content only.
- The system must store syllabus chunks as embeddings in a vector database.
- The system must retrieve relevant content using semantic similarity.
- The system must generate answers strictly grounded in retrieved syllabus content.
- The system must apply fixed prompting to ensure consistency.


### 3.6 Text-to-Speech (TTS)

- The system must convert generated text responses into natural speech.
- The TTS must provide clear pronunciation of:
  - Formulas
  - Scientific terms
  - Mathematical expressions
- The system must support pause, resume, and repeat functionality.

### 3.7 Accessibility Requirements

- The system must be fully operable through voice commands.
- The system must not require visual interaction for core functionality.
- The system must be compatible with screen readers.
- The system must support assistive technologies.

## 4. Non-Functional Requirements

### 4.1 Performance

- The system must provide responses within 3 seconds (average latency).
- Lecture streaming must be smooth without interruptions.
- The system must handle concurrent users efficiently.


### 4.2 Accuracy

- The system must minimize hallucinated responses.
- All generated answers must be grounded in syllabus content.
- The system must maintain consistency across similar question phrasings.


### 4.3 Scalability

- The system must support cloud-based scaling.
- The architecture must allow onboarding of multiple classes and boards.
- The system must support expansion to regional languages.

### 4.4 Reliability

- The system must ensure high uptime (> 99% availability).
- The system must handle network interruptions gracefully.
- The system must log errors for monitoring and debugging.


### 4.5 Security & Privacy

- The system must not store sensitive user data without consent.
- Voice input data must be securely processed.
- Backend APIs must be protected using authentication mechanisms.


## 5. Target Users

### Primary Users
- Visually impaired school students (Class 6–12)

### Secondary Users
- Teachers (future dashboard integration)
- Educational institutions
- NGOs working in inclusive education


## 6. Constraints

- Initial version focuses on one educational board.
- Internet connectivity required (offline mode in future scope).
- Prototype deployment on cloud infrastructure.

## 7. Success Criteria

- Students can independently navigate syllabus via voice.
- Doubts are answered accurately using syllabus-grounded responses.
- Users can complete a full chapter without visual assistance.
- System demonstrates measurable reduction in dependency on external help.

