# RAG System for ROS2 Navigation - Project Overview

## Model Information

We have fine-tuned a text-generation model for answering questions related to ROS2 navigation, motion planning, and simulation.

**[Link to the Finetuned Trained Model](https://huggingface.co/ChaosKingNV/finetuned-ros2-model)**

---

## Project File Structure

```
RAG-Project/
├── app/                   # Main application directory
│   ├── app.py             # FastAPI application for API services
│   ├── gradio_app.py      # Gradio application for user interface
│   ├── Dockerfile         # Dockerfile for container setup
│   ├── requirements.txt   # Python dependencies
│   └── docker-compose.yml # Docker Compose configuration
│
├── etl/                   # ETL Pipeline for data extraction
│   ├── etl_pipeline.py    # Main ETL logic
│   └── config.py          # ETL configuration
│
├── featurization/         # Data featurization pipeline
│   ├── featurizer.py      # Vector embedding generation
│   ├── featurization_pipeline.py
│   └── config.py          # Featurization config
│
├── youtube_pipeline/      # YouTube data extraction and labeling
│   ├── youtube_transcript_collector.py
│   ├── question_answer_generator.py
│   └── config.py
│
├── finetuning/            # Model fine-tuning pipeline
│   ├── data_preprocessor.py
│   ├── model_trainer.py
│   ├── upload_to_hub.py
│   ├── config.py          # Fine-tuning configuration
│   └── clearml_tracker.py
│
├── clearml_integration/   # ClearML integration for experiment tracking
│   └── clearml_tracker.py
│
└── static/                # Static files and assets
    └── ...
```

---

## How It Works

1. **ETL Pipeline:** Extracts relevant data from YouTube videos and official ROS2 documentation.
2. **Featurization:** Converts raw data into vector embeddings using a Sentence Transformer model.
3. **Fine-Tuning:** Trains a Hugging Face model using labeled Q/A pairs generated during data processing.
4. **Model Deployment:** Uploads the trained model to Hugging Face Hub and registers it with ClearML for experiment tracking.
5. **Query System:**
   - **FastAPI API:** Handles API requests for querying the model.
   - **Gradio Interface:** Provides a user-friendly web interface.
   - **Vector Search:** Retrieves relevant documents from Qdrant based on query embeddings.
   - **Answer Generation:** Combines search results with the model’s capabilities to generate answers.

---

## How to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository/rag-project.git
   cd rag-project
   ```

2. **Start the Docker Containers:**
   ```bash
   docker-compose up --build
   ```

3. **Access the System:**
   - **API Endpoint:** `http://localhost:8000`
   - **Gradio Web App:** `http://localhost:7860`

---
## Screenshots

![SS1](SS/SS1.jpg)
![SS2](SS/SS2.jpg)
![SS3](SS/SS3.jpg)

## Project Description

### Overview
The **Retrieval Augmented Generation (RAG)** system is designed to assist ROS2 robotics developers with navigation stack development for agents with egomotion. The system focuses on specific subdomains, including:

- **ROS2 robotics middleware**
- **Nav2 navigation**
- **Movit2 motion planning**
- **Gazebo simulation**

RAG combines retrieval-based and generation-based models, allowing it to retrieve relevant information from large corpora and generate domain-specific responses.

---

### Project Goals & Strategy
The goal is to build a RAG system capable of answering specific questions regarding ROS2 navigation and related topics. We will implement the system iteratively, continuously improving its components. Initial iterations focus on integration, with further refinements in subsequent milestones.

---

### Milestones

#### 1. Environment and Tooling Milestone
- **Objective:** Set up a development environment using Docker Compose.
- **Components:**
  - **App:** For model training, serving, and API interactions.
  - **MongoDB:** Database for storing raw RAG data after ETL.
  - **Qdrant:** Vector search engine for the RAG system.
  - **ClearML:** Experiment tracker and orchestrator.

#### 2. ETL Milestone
- **Objective:** Build an ETL pipeline to ingest ROS2 documentation and YouTube videos.
- **Important:** Only CS370 Honors and CS-GY-6613 students need to handle video transcripts.
- **Tool:** ClearML orchestrator to automate data ingestion and storage in MongoDB.

#### 3. Featurization Pipeline Milestone
- **Objective:** Implement a featurization pipeline to convert raw data into vectors.
- **Tool:** Sentence Transformer model for vector embedding generation.
- **Output:** Featurized data stored in MongoDB and Qdrant.

#### 4. Fine-Tuning Milestone
- **Objective:** Fine-tune a pre-trained Hugging Face model on the ROS2 subdomains.
- **Important:** Only CS370 Honors and CS-GY-6613 students are required to perform fine-tuning.
- **Tool:** Utilize existing fine-tuning tutorials, Google Colab, or other cloud services for model training.

#### 5. Deploying the App Milestone
- **Objective:** Develop a Gradio app for user interaction with the RAG system.
- **Features:**
  - Pre-populated questions related to ROS2 navigation.
  - Use Ollama and Hugging Face Hub to pull the fine-tuned model.

- **Example Questions:**
  - "How can I navigate to a specific pose? Include replanning aspects in your answer."
  - "Can you provide me with code for this task?"

---

### Technologies & Tools Used
- **FastAPI:** For building the API endpoints.
- **Gradio:** For the user interface.
- **Docker:** For containerized deployment.
- **MongoDB:** For storing raw data.
- **Qdrant:** For vector search functionality.
- **ClearML:** For experiment tracking and orchestration.
- **Sentence Transformers:** For featurization (vector embeddings).
- **Hugging Face:** For model fine-tuning and hosting.

