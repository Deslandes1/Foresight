import streamlit as st
import asyncio
import tempfile
import base64
import os
import subprocess
from datetime import datetime

st.set_page_config(page_title="Foresight – AI & Robotics Insights", layout="wide")

# ---------- Language data (only English for now, easy to extend) ----------
LANGUAGES = {
    "English": {
        "code": "en",
        "voice": "en-US-GuyNeural",
        "login_title": "🔐 Access Required",
        "login_sub": "20 essential insights – AI, LLMs, robotics & the future",
        "login_password": "Enter password to access",
        "login_btn": "Login",
        "login_error": "Incorrect password. Access denied.",
        "sidebar_progress": "Your progress",
        "sidebar_completed": "of 20",
        "sidebar_founder": "Founder & Developer:",
        "sidebar_price": "**$49 USD** (complete insights, source code included)",
        "sidebar_logout": "Logout",
        "module_prefix": "Module",
        "duration_label": "Reading time",
        "next_module": "Next Module",
        "prev_module": "Previous Module",
        "download_btn": "📥 Download Notes (TXT)",
        "footer_caption": "🤖 Foresight – 20 insights to stay ahead of the curve."
    }
}

# ---------- 20 modules with title, content, image URL ----------
modules_data = {
    1: {
        "title": "How Large Language Models (LLMs) Actually Work",
        "content": """
        **The Transformer Architecture**  
        Large Language Models like GPT-4, Gemini, and Claude are built on a deep learning architecture called the Transformer. Unlike older recurrent networks, Transformers process all words in a sentence simultaneously using a mechanism called "self-attention". This allows the model to understand context and relationships between words, regardless of their distance in the text.  
        
        **Training Process**  
        LLMs are trained in two main stages: pre-training and fine-tuning. During pre-training, the model learns to predict the next word in a huge corpus of internet text (billions of pages). It develops grammar, facts, reasoning patterns, and even biases. Fine-tuning then adjusts the model for specific tasks like conversation or coding, often using human feedback (RLHF).  
        
        **Why Scale Matters**  
        Larger models with more parameters (hundreds of billions) tend to perform better, but they also require massive computational resources. Recent research shows that data quality and training efficiency can be as important as raw size.  
        
        **Limitations**  
        LLMs can "hallucinate" (make up confident-sounding but false information), have limited context windows (typically 8k-128k tokens), and reflect the biases in their training data. Understanding these limits is crucial for responsible use.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Transformer_architecture.png/800px-Transformer_architecture.png",
        "audio_text": "How Large Language Models work. Transformers use self-attention to process words simultaneously. Training involves pre-training and fine-tuning. Larger models perform better but have limitations like hallucinations and context windows."
    },
    2: {
        "title": "The Rise of Dexterous Robotics – BrainCo's Hand",
        "content": """
        **What Makes BrainCo's Hand Different**  
        Most industrial robots use simple grippers that can only pick and place objects. BrainCo's new dexterous hand has five independently articulated fingers, each with multiple joints. It can perform fine motor tasks: holding a pen, turning a key, even playing musical instruments.  
        
        **How It Works**  
        The hand uses a combination of electric motors, tendon-like cables, and force sensors. Machine learning algorithms translate human movements (captured by a sensor glove) into precise finger motions. The system can also operate autonomously using computer vision to identify and grasp objects of various shapes.  
        
        **Implications for Automation**  
        Tasks that once required human dexterity – assembling electronics, handling delicate medical instruments, sorting irregular packages – are now within reach of automation. Industries like healthcare, logistics, and manufacturing will see major shifts in the next 3-5 years.  
        
        **Challenges**  
        Cost (currently high), durability, and the need for advanced AI control systems remain barriers. However, rapid progress suggests that dexterous robots will become commercially viable sooner than many expect.
        """,
        "image": "https://www.brainco.tech/hubfs/BrainCo_Robotic_Hand.jpg",
        "audio_text": "BrainCo's dexterous robotic hand mimics human fine motor skills. It uses articulated fingers, force sensors, and AI. Applications in healthcare, assembly, and logistics. Challenges remain but progress is rapid."
    },
    3: {
        "title": "The Future of AI Agents – From Chatbots to Action",
        "content": """
        **What Are AI Agents?**  
        Unlike chatbots that only respond to prompts, AI agents are designed to take actions: book flights, send emails, control smart home devices, even write and execute code. They combine LLMs with tools and APIs.  
        
        **How They Work**  
        An agent receives a goal (e.g., "plan a trip to Paris"). It breaks the task into steps, decides which tools to use (search, calendar, booking API), executes actions, and learns from results. This loop of reasoning, acting, and observing is called "ReAct" (Reasoning + Acting).  
        
        **Current Examples**  
        AutoGPT, BabyAGI, and LangChain agents are early prototypes. Companies like Adept and Google are building more robust versions for enterprise automation.  
        
        **Potential and Risks**  
        Agents could automate entire workflows, but they also pose risks: executing harmful actions if not properly constrained, making costly mistakes, and being difficult to debug. Safe deployment requires careful guardrails.
        """,
        "image": "https://via.placeholder.com/800x400?text=AI+Agents+Illustration",
        "audio_text": "AI agents go beyond chatbots – they take actions. They use reasoning loops and tools. Examples include AutoGPT. Potential to automate workflows but risks need careful management."
    },
    4: {
        "title": "Multimodal AI – Seeing, Hearing, and Understanding",
        "content": """
        **Beyond Text**  
        Multimodal AI models can process and generate not just text, but also images, audio, and video. GPT-4 with vision, Google Gemini, and Meta's ImageBind are leading examples.  
        
        **How It Works**  
        These models are trained on vast datasets containing paired modalities: images with captions, video with audio, etc. They learn to map different types of data into a shared semantic space. For instance, they can understand that a picture of a cat and the word "cat" are related.  
        
        **Applications**  
        - Medical diagnosis: analyzing X‑rays and patient notes together.  
        - Accessibility: describing scenes for blind users.  
        - Content creation: generating videos from text descriptions.  
        
        **Challenges**  
        Training is computationally expensive. Aligning different modalities without losing information is difficult. Bias can propagate across all modalities.
        """,
        "image": "https://via.placeholder.com/800x400?text=Multimodal+AI",
        "audio_text": "Multimodal AI processes text, images, audio, and video. Models like GPT-4 Vision and Gemini are examples. Applications in medicine, accessibility, and content creation. Challenges include cost and bias."
    },
    5: {
        "title": "Edge AI – Running Models on Your Phone",
        "content": """
        **Why Edge AI Matters**  
        Most AI runs in the cloud, which requires internet and causes latency. Edge AI runs models directly on devices: smartphones, cameras, cars, even microcontrollers. This enables real‑time processing, privacy, and offline operation.  
        
        **Techniques**  
        - Model compression (pruning, quantization) to reduce size.  
        - Specialized hardware like Google's TPU, Apple's Neural Engine, and NVIDIA Jetson.  
        - On‑device training (federated learning) for personalization without sending data to the cloud.  
        
        **Examples**  
        - Face unlock on phones.  
        - Real‑time translation without internet.  
        - Anomaly detection in industrial equipment.  
        
        **Future**  
        As chips become more powerful, more complex models will run at the edge, reducing reliance on cloud servers and enabling new applications like autonomous drones and smart sensors.
        """,
        "image": "https://via.placeholder.com/800x400?text=Edge+AI",
        "audio_text": "Edge AI runs models on local devices, not the cloud. It enables real-time processing, privacy, and offline use. Techniques include compression and specialized hardware. Examples: face unlock, offline translation."
    },
    6: {
        "title": "AI Hallucinations – Why Models Make Things Up",
        "content": """
        **What Are Hallucinations?**  
        When an LLM generates plausible-sounding but factually incorrect or nonsensical information, it's called a hallucination. For example, inventing a scientific paper that doesn't exist or citing wrong dates.  
        
        **Why Do They Happen?**  
        LLMs are trained to predict the next most likely word, not to assert truth. They have no internal knowledge base to verify facts. Hallucinations are more common when the prompt is ambiguous, asks for obscure information, or pushes the model beyond its training data.  
        
        **Mitigation Strategies**  
        - Retrieval-Augmented Generation (RAG): provide relevant documents as context.  
        - Chain-of-thought prompting: force step‑by‑step reasoning.  
        - Fine-tuning with high‑quality, verified data.  
        - Using external fact-checking tools.  
        
        **Why It's Still Unsolved**  
        Eliminating hallucinations entirely would require a model that understands truth – a very hard problem. Current best practice is to design applications that can tolerate or detect hallucinations.
        """,
        "image": "https://via.placeholder.com/800x400?text=AI+Hallucinations",
        "audio_text": "Hallucinations are when AI makes up false information. They happen because models predict likely words, not facts. Mitigation includes RAG and fine-tuning. Complete elimination is still unsolved."
    },
    7: {
        "title": "Reinforcement Learning from Human Feedback (RLHF)",
        "content": """
        **What Is RLHF?**  
        RLHF is a technique used to align LLMs with human preferences. After pre-training, the model is fine-tuned using feedback from human evaluators who rank different model outputs. This helps the model learn what responses are helpful, honest, and harmless.  
        
        **How It Works**  
        1. A human ranks two or more model outputs.  
        2. A reward model is trained to predict human preferences.  
        3. The LLM is fine‑tuned using reinforcement learning (often PPO) to maximize the reward model's score.  
        
        **Why It's Important**  
        RLHF reduces harmful outputs, improves helpfulness, and makes models more engaging. It's why ChatGPT feels more "aligned" than base GPT-3.  
        
        **Limitations**  
        RLHF is expensive and time‑consuming. It can also introduce new biases based on the preferences of the human evaluators. Scaling it to all possible scenarios is impossible.
        """,
        "image": "https://via.placeholder.com/800x400?text=RLHF",
        "audio_text": "RLHF aligns AI with human preferences. Humans rank outputs, a reward model learns, and the LLM is fine-tuned. It reduces harm and improves helpfulness but is expensive and can introduce bias."
    },
    8: {
        "title": "The Economics of AI – Cost, Compute, and Carbon",
        "content": """
        **The True Cost of AI**  
        Training a large LLM like GPT-4 costs tens of millions of dollars in compute (GPU hours) and electricity. Inference (using the model) also adds up: serving millions of users requires vast server farms.  
        
        **Compute Trends**  
        Compute demand for AI has doubled every ~3.4 months since 2012, far outpacing Moore's Law. This drives investment in specialized hardware like GPUs, TPUs, and neuromorphic chips.  
        
        **Carbon Footprint**  
        Training a single large model can emit as much carbon as five cars over their lifetimes. However, inference (usage) over the model's life may account for far more. Companies are increasingly using carbon‑aware scheduling and renewable energy.  
        
        **Making AI More Affordable**  
        Techniques like distillation (training smaller models to mimic larger ones), quantization, and efficient architectures (Mixture of Experts) help reduce costs. Open‑source models also democratize access.
        """,
        "image": "https://via.placeholder.com/800x400?text=AI+Economics",
        "audio_text": "Training large AI models costs millions of dollars and significant carbon. Compute demand grows faster than Moore's Law. Techniques like distillation and efficient architectures help reduce costs."
    },
    9: {
        "title": "Retrieval-Augmented Generation (RAG)",
        "content": """
        **What Is RAG?**  
        RAG combines an LLM with an external knowledge base (e.g., a database, vector store, or search engine). When asked a question, the system first retrieves relevant documents, then feeds them as context to the LLM to generate an answer grounded in those sources.  
        
        **Why Use RAG?**  
        - Reduces hallucinations by providing factual references.  
        - Keeps knowledge up‑to‑date without retraining the model.  
        - Allows the model to access private or proprietary data.  
        
        **How It Works**  
        1. User asks a question.  
        2. A retriever (e.g., dense vector search) finds relevant chunks from a knowledge base.  
        3. The LLM receives the question + retrieved chunks and generates an answer citing the sources.  
        
        **Applications**  
        Customer support (company documentation), research assistants (academic papers), legal analysis (case law), and any domain requiring up‑to‑date, verifiable information.
        """,
        "image": "https://via.placeholder.com/800x400?text=RAG+Diagram",
        "audio_text": "RAG combines LLMs with external knowledge bases. It retrieves relevant documents then generates answers grounded in them. Reduces hallucinations and keeps knowledge current. Used in support, research, legal."
    },
    10: {
        "title": "Open‑Source vs. Proprietary AI Models",
        "content": """
        **The Landscape**  
        Proprietary models (GPT-4, Claude, Gemini) are developed by companies, kept secret, and accessed via APIs. Open‑source models (Llama, Mistral, Falcon) have weights publicly available and can be run locally.  
        
        **Pros and Cons**  
        | Aspect | Proprietary | Open‑Source |  
        |--------|-------------|-------------|  
        | Performance | Usually state‑of‑the‑art | Often slightly behind |  
        | Cost | Pay per token | Free (except compute) |  
        | Privacy | Data may be logged | Full control |  
        | Customization | Limited | Full fine‑tuning |  
        | Transparency | Black box | Inspectable |  
        
        **The Open‑Source Advantage**  
        Open‑source models allow researchers to study biases, developers to build on‑premise solutions, and startups to avoid API costs. The gap in capability is closing rapidly, with Llama 3 and Mixtral approaching GPT-4 performance on many benchmarks.  
        
        **Future**  
        The trend suggests open‑source models will become increasingly competitive, forcing proprietary providers to offer more value (e.g., better tooling, safety guarantees, or integration).
        """,
        "image": "https://via.placeholder.com/800x400?text=Open+Source+vs+Proprietary",
        "audio_text": "Open-source models like Llama are free and customizable but slightly behind proprietary models like GPT-4. Proprietary models are state-of-the-art but cost money and lack transparency. The gap is closing."
    },
    11: {
        "title": "AI in Healthcare – Diagnosis, Drug Discovery, and Beyond",
        "content": """
        **Diagnosis**  
        AI models can now detect diseases from medical images (X‑rays, MRIs, retinal scans) with accuracy rivaling or exceeding human experts. For example, Google's LYNA detects breast cancer metastases, and IDx‑DR diagnoses diabetic retinopathy.  
        
        **Drug Discovery**  
        AlphaFold solved the protein folding problem, predicting 3D structures from amino acid sequences. This accelerates drug design. Generative models can also propose novel molecules for specific targets, reducing discovery time from years to months.  
        
        **Personalized Medicine**  
        LLMs can analyze patient records, genetic data, and clinical studies to recommend tailored treatments. They also power chatbots that triage symptoms and answer patient questions, reducing clinician workload.  
        
        **Challenges**  
        Regulatory approval, data privacy (HIPAA), and avoiding bias are major hurdles. AI systems must be rigorously validated before clinical deployment.
        """,
        "image": "https://via.placeholder.com/800x400?text=AI+in+Healthcare",
        "audio_text": "AI helps diagnose diseases from medical images, discovers new drugs via AlphaFold, and enables personalized medicine. Challenges include regulation, privacy, and bias."
    },
    12: {
        "title": "Generative AI for Video – Runway, Sora, and the Future",
        "content": """
        **From Text to Video**  
        Generative video models like Runway's Gen‑2, OpenAI's Sora, and Pika Labs can create short video clips from text prompts. They learn the dynamics of real‑world motion, lighting, and objects.  
        
        **How They Work**  
        These models are typically diffusion‑based (like image generators) but extended to the temporal dimension. They are trained on vast datasets of video clips with captions, learning to predict subsequent frames.  
        
        **Current Capabilities**  
        - Generate up to 10‑60 seconds of consistent video.  
        - Animate static images.  
        - Extend or edit existing videos.  
        
        **Limitations**  
        Physics can still be inconsistent (objects passing through each other). Long‑range coherence (story over minutes) is not yet possible. Compute cost is high.  
        
        **Implications**  
        Film production, advertising, and social media will be transformed. Soon, anyone will be able to create short films from a script.
        """,
        "image": "https://via.placeholder.com/800x400?text=Generative+Video",
        "audio_text": "Generative video models like Runway and Sora create clips from text. They use diffusion extended to time. Current limits: short clips, occasional physics glitches. Future impact on film and ads."
    },
    13: {
        "title": "AI Safety – Alignment, Robustness, and Control",
        "content": """
        **Alignment Problem**  
        How do we ensure AI systems pursue goals that are beneficial to humans? Misaligned AI could optimize for the wrong objective (e.g., a paperclip maximizer). Current alignment techniques include RLHF, constitutional AI, and scalable oversight.  
        
        **Robustness**  
        AI systems can be fooled by adversarial examples – small, imperceptible changes to input that cause wrong outputs. Robustness research aims to make models resistant to such attacks.  
        
        **Control and Monitoring**  
        For advanced AI, we may need methods to verify behavior, shut down unsafe systems, and prevent deception. This includes interpretability (understanding why a model made a decision) and anomaly detection.  
        
        **Why It Matters Now**  
        Even today's LLMs can be jailbroken to produce harmful content. As AI becomes more capable and autonomous, safety research becomes urgent. Leading labs have dedicated safety teams, but the field is still young.
        """,
        "image": "https://via.placeholder.com/800x400?text=AI+Safety",
        "audio_text": "AI safety covers alignment (ensuring AI pursues human goals), robustness (resistance to adversarial attacks), and control. Even current models can be jailbroken. Research is urgent as AI advances."
    },
    14: {
        "title": "The Turing Test and Beyond – Measuring Intelligence",
        "content": """
        **The Turing Test**  
        Proposed by Alan Turing in 1950, a machine passes if a human cannot distinguish its responses from a human's. Today, many LLMs can easily pass the original test, but the test is now considered insufficient for true intelligence.  
        
        **Modern Benchmarks**  
        - MMLU (Massive Multitask Language Understanding) – tests knowledge across 57 subjects.  
        - GSM8K – grade school math problems.  
        - HumanEval – code generation.  
        - BIG‑bench – diverse reasoning tasks.  
        
        **What's Missing**  
        Current benchmarks don't measure long‑term planning, memory, embodiment, or social intelligence. Some argue that intelligence is not a single dimension but a collection of capabilities.  
        
        **Future Directions**  
        Researchers are developing more holistic evaluations, including interactive environments (like Minecraft) where agents must achieve goals over extended periods.
        """,
        "image": "https://via.placeholder.com/800x400?text=Turing+Test",
        "audio_text": "The Turing Test is outdated. Modern benchmarks include MMLU, GSM8K, and HumanEval. They measure knowledge, math, and code. Future evaluations will include long-term planning and embodiment."
    },
    15: {
        "title": "Low‑Code and No‑Code AI for Everyone",
        "content": """
        **Democratizing AI**  
        Platforms like Microsoft Power Automate, Zapier, and Make allow users to build AI‑powered workflows without writing code. Drag‑and‑drop interfaces connect apps, trigger actions, and integrate AI models.  
        
        **What You Can Build**  
        - Automatically summarize emails.  
        - Classify customer support tickets.  
        - Extract data from invoices.  
        - Generate social media posts.  
        
        **Benefits**  
        Non‑technical employees can automate tasks, reducing workload and errors. Businesses can quickly prototype AI solutions without hiring developers.  
        
        **Limitations**  
        These tools are limited to pre‑built connectors and templates. Custom logic or complex models still require coding. However, the trend is toward more flexibility and power.
        """,
        "image": "https://via.placeholder.com/800x400?text=Low+Code+AI",
        "audio_text": "Low-code AI platforms like Zapier and Make let non-technical users build automations. Benefits include speed and accessibility. Limitations: custom logic still requires coding."
    },
    16: {
        "title": "Ethical AI – Bias, Fairness, and Transparency",
        "content": """
        **Sources of Bias**  
        AI models inherit biases from their training data (e.g., stereotypes in text, underrepresentation in images). They can also amplify those biases, leading to unfair outcomes in hiring, lending, policing, etc.  
        
        **Measuring Fairness**  
        There are multiple definitions: demographic parity (equal outcomes across groups), equal opportunity (equal true positive rates), and individual fairness (similar individuals get similar predictions). No single metric is universally correct.  
        
        **Mitigation Strategies**  
        - Pre‑processing: debias training data.  
        - In‑processing: add fairness constraints during training.  
        - Post‑processing: adjust model outputs.  
        
        **Transparency**  
        Explainable AI (XAI) methods like LIME and SHAP help users understand why a model made a decision. However, for large neural networks, full interpretability remains an open problem.  
        
        **Regulation**  
        The EU's AI Act and similar regulations require risk assessments and transparency for high‑risk AI systems. Companies must audit models for bias.
        """,
        "image": "https://via.placeholder.com/800x400?text=Ethical+AI",
        "audio_text": "AI bias comes from training data. Fairness can be measured in different ways. Mitigation includes debiasing and constraints. Transparency tools like LIME help explain decisions. Regulations are emerging."
    },
    17: {
        "title": "The Future of Work with AI – Augmentation, Not Replacement",
        "content": """
        **Historical Patterns**  
        Automation has always displaced some jobs while creating new ones. The printing press, steam engine, and computer each caused upheaval, but employment eventually grew.  
        
        **AI's Unique Impact**  
        AI affects cognitive work – writing, coding, design, analysis. It can augment workers by handling routine subtasks, allowing humans to focus on higher‑value activities (creativity, strategy, relationships).  
        
        **Which Jobs Are Most Exposed?**  
        Research suggests that jobs involving data processing, pattern recognition, and routine communication are most affected. Physical jobs are less exposed (for now). However, dexterous robotics is closing that gap.  
        
        **What Workers Can Do**  
        - Learn to use AI tools as co‑pilots.  
        - Develop soft skills (empathy, communication, leadership).  
        - Embrace lifelong learning.  
        
        **Organizational Response**  
        Companies should invest in reskilling, redesign workflows, and involve workers in AI adoption decisions.
        """,
        "image": "https://via.placeholder.com/800x400?text=Future+of+Work",
        "audio_text": "AI will augment, not replace, most jobs. It automates routine cognitive tasks. Workers should learn AI tools and soft skills. Organizations must reskill and redesign workflows."
    },
    18: {
        "title": "Quantum Machine Learning – Hype or Reality?",
        "content": """
        **What Is Quantum Machine Learning?**  
        QML uses quantum computers to speed up machine learning algorithms. Potential applications include solving linear systems exponentially faster, improving optimization, and discovering new materials.  
        
        **Current State**  
        Quantum computers are still small (noisy, limited qubits). Only a few toy demonstrations exist, such as quantum kernel methods or small Boltzmann machines. No practical advantage has been proven yet.  
        
        **Challenges**  
        - Hardware instability (decoherence).  
        - Lack of quantum RAM to load classical data.  
        - Algorithm design is extremely difficult.  
        
        **When Will It Arrive?**  
        Most experts believe practical QML is at least a decade away, and it may only benefit specific niches (e.g., chemistry, optimization). Classical AI will remain dominant for the foreseeable future.
        """,
        "image": "https://via.placeholder.com/800x400?text=Quantum+Machine+Learning",
        "audio_text": "Quantum machine learning promises speedups for some algorithms, but current quantum computers are too small. Practical QML is likely a decade away. Classical AI remains dominant."
    },
    19: {
        "title": "Embodied AI – Robots That Learn in the Real World",
        "content": """
        **Beyond Pure Software**  
        Embodied AI gives an AI a body – a robot, drone, or even a simulated avatar. It learns by interacting with the physical world through sensors and actuators.  
        
        **Challenges**  
        - Real‑world interaction is slow and expensive compared to simulation.  
        - Sim‑to‑real transfer is hard because of physical differences.  
        - Safety constraints prevent random exploration.  
        
        **Recent Advances**  
        - Google's RT-2: a vision‑language‑action model that can follow commands in novel situations.  
        - Meta's Habitat: simulated environments for training navigation agents.  
        - Reinforcement learning from human feedback (RLHF) in robotics.  
        
        **Applications**  
        Warehouse automation, domestic service robots, search and rescue, and space exploration. Embodied AI could eventually lead to general‑purpose household robots.
        """,
        "image": "https://via.placeholder.com/800x400?text=Embodied+AI",
        "audio_text": "Embodied AI gives intelligence a physical body. It learns by interacting with the real world. Challenges include slow learning and sim-to-real transfer. Recent advances include Google's RT-2."
    },
    20: {
        "title": "How to Stay Ahead – Lifelong Learning in the AI Era",
        "content": """
        **The Pace of Change**  
        AI capabilities are doubling every few months. What was cutting‑edge a year ago is now standard. To stay relevant, you need a strategy for continuous learning.  
        
        **Practical Tips**  
        - Follow key researchers and labs (OpenAI, DeepMind, Stanford).  
        - Build small projects using new APIs (OpenAI, Hugging Face).  
        - Join communities (Reddit, Discord, local meetups).  
        - Set aside 2‑4 hours weekly for reading and experimentation.  
        
        **What to Learn**  
        - Prompt engineering and AI tool usage.  
        - Basic Python and API integration.  
        - Understanding model limitations and evaluation.  
        - Ethical and legal aspects of AI deployment.  
        
        **The Mindset**  
        Don't try to master everything. Focus on learning how to learn – adapt quickly to new tools as they emerge. The most valuable skill is not knowing a specific technology but being able to pick it up when needed.
        """,
        "image": "https://via.placeholder.com/800x400?text=Lifelong+Learning",
        "audio_text": "Stay ahead by continuous learning. Follow researchers, build small projects, join communities. Learn prompt engineering, basic Python, and ethical considerations. The key skill is learning how to learn."
    }
}

# ---------- Helper functions ----------
def set_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0a0f1f, #0e1a2a, #0a0f1f); }
        .main-header { background: linear-gradient(135deg, #00d4ff, #0077ff, #0033aa); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, pre, code, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: #ffffff !important; }
        .stText { color: #ffffff !important; font-size: 1rem; background: transparent !important; }
        .stButton button { background-color: #0077ff; color: white !important; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #00d4ff; color: black !important; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0a0f1f, #0e1a2a); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #1e2a3a; border: 1px solid #0077ff; border-radius: 10px; }
        div[data-baseweb="popover"] ul { background-color: #1e2a3a; border: 1px solid #0077ff; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #1e2a3a; }
        div[data-baseweb="popover"] li:hover { background-color: #0077ff; }
        .module-image { border-radius: 15px; margin: 1rem 0; width: 100%; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#00d4ff" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00d4ff"/>
                    <stop offset="50%" stop-color="#0077ff"/>
                    <stop offset="100%" stop-color="#0033aa"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">🔭</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

def generate_audio(text, output_path, voice):
    clean_text = ' '.join(text.split())
    cmd = ["edge-tts", "--voice", voice, "--text", clean_text, "--write-media", output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
        return True
    except:
        return False

def play_audio(text, key, voice):
    if st.button(f"🔊 Listen", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            success = generate_audio(text, tmp.name, voice)
            if success:
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            os.unlink(tmp.name)

# ---------- Authentication ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "module_index" not in st.session_state:
    st.session_state.module_index = 0

if not st.session_state.authenticated:
    set_style()
    lang = st.session_state.lang
    ui = LANGUAGES[lang]
    st.title(ui["login_title"])
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Foresight</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #00d4ff;'>{ui['login_sub']}</p>", unsafe_allow_html=True)
        password_input = st.text_input(ui["login_password"], type="password")
        if st.button(ui["login_btn"]):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(ui["login_error"])
    st.stop()

# ---------- Main app ----------
set_style()
lang = st.session_state.lang
ui = LANGUAGES[lang]
voice = ui["voice"]

# Language selector in sidebar
with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=60)
    st.selectbox("🌐 Language", options=list(LANGUAGES.keys()), key="lang")
    st.markdown("---")
    show_logo()
    st.markdown(f"## 🎯 {ui['module_prefix']}")
    module_number = st.selectbox("", list(range(1, 21)), index=st.session_state.module_index, format_func=lambda x: f"{ui['module_prefix']} {x}: {modules_data[x]['title'][:40]}...", label_visibility="collapsed")
    st.session_state.module_index = module_number - 1
    st.markdown("---")
    st.markdown(f"### 📚 {ui['sidebar_progress']}")
    st.progress(module_number / 20)
    st.markdown(f"✅ {ui['module_prefix']} {module_number} {ui['sidebar_completed']}")
    st.markdown("---")
    st.markdown(f"**{ui['sidebar_founder']}**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown(ui['sidebar_price'])
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button(f"🚪 {ui['sidebar_logout']}", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ---------- Display current module ----------
module = modules_data[module_number]
st.markdown(f"## {ui['module_prefix']} {module_number}: {module['title']}")
st.markdown("---")

# Display image
try:
    st.image(module['image'], use_container_width=True, caption=module['title'])
except:
    st.info("🖼️ Image not available – you can replace the URL in the code.")

st.markdown(module['content'])

# Audio and download buttons
col1, col2 = st.columns(2)
with col1:
    play_audio(module['audio_text'], f"audio_{module_number}", voice)
with col2:
    if st.button(ui['download_btn'], use_container_width=True):
        # Create notes file
        notes = f"Module {module_number}: {module['title']}\n\n{module['content']}\n\n---\nGenerated by Foresight – GlobalInternet.py"
        st.download_button("⬇️ Download", notes, file_name=f"foresight_module_{module_number}.txt", mime="text/plain")

# Navigation buttons
col_prev, col_next = st.columns(2)
with col_prev:
    if module_number > 1:
        if st.button(f"⬅️ {ui['prev_module']}", use_container_width=True):
            st.session_state.module_index = module_number - 2
            st.rerun()
with col_next:
    if module_number < 20:
        if st.button(f"{ui['next_module']} ➡️", use_container_width=True):
            st.session_state.module_index = module_number
            st.rerun()

if module_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 You have completed all 20 insights.")
    st.markdown("""
    ### 📞 To get more advanced content or support:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Keep learning – the future belongs to those who understand AI and robotics.
    """)

st.markdown("---")
st.caption(ui['footer_caption'])
