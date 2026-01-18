# RAG Chatbot User Guide

## Welcome! 👋

This guide will help you get started with the RAG Chatbot application and make the most of its features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Using the Web Interface](#using-the-web-interface)
3. [Using the Command Line](#using-the-command-line)
4. [Managing Documents](#managing-documents)
5. [Tips for Better Results](#tips-for-better-results)
6. [Common Questions](#common-questions)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Time Setup

1. **Install the application** (see README.md for detailed instructions)
2. **Set up your API key** in `main.py`
3. **Add your documents** to the `data/` folder
4. **Start the application**

### Quick Start

```bash
# Start the web interface
python main.py --web

# Open your browser to http://localhost:5000
```

That's it! You're ready to start chatting.

---

## Using the Web Interface

### Main Interface Overview

The web interface has two main sections:

#### Left Panel: Chat Interface
- **Robot Animation**: Shows when the bot is thinking
- **Chat Messages**: Your conversation history
- **Input Field**: Where you type your questions
- **Top-K Control**: Adjusts how many documents to retrieve
- **Send Button**: Submits your question

#### Right Panel: Document Management
- **Upload Section**: Add new documents
- **Reindex Button**: Rebuild the search index
- **Status Display**: Shows current operation status
- **Last Context**: Shows which documents were used for the last answer

### Asking Questions

1. **Type your question** in the input field at the bottom
2. **Press Enter** or click the "Send" button
3. **Wait for the response** (the robot will animate while thinking)
4. **View the answer** in the chat area
5. **Check the context** in the right panel to see which documents were used

#### Example Questions

Good questions are:
- ✅ "What is Kubernetes?"
- ✅ "How do I deploy a Docker container?"
- ✅ "Explain the difference between pods and nodes"
- ✅ "What are the benefits of microservices?"

Less effective questions:
- ❌ "Tell me everything" (too broad)
- ❌ "Yes" (no context)
- ❌ "What?" (unclear)

### Adjusting Top-K

The **Top-K** setting controls how many document chunks are retrieved:

- **Lower values (1-3)**: More focused, faster responses
- **Higher values (4-7)**: More comprehensive, may include less relevant info
- **Very high values (8-10)**: Maximum context, but may be slower

**Recommendation**: Start with 3-4 and adjust based on your needs.

### Uploading Documents

1. **Click "Choose File"** in the Documents section
2. **Select your document** (supports .txt, .md, .csv, .pdf, .docx)
3. **Click "Upload & Index"**
4. **Wait for confirmation** in the status area
5. **Start asking questions** about your new document!

**Note**: The system automatically reindexes after each upload.

### Reindexing

Use the **Reindex** button when:
- You've manually added files to the `data/` folder
- You've deleted documents
- The search results seem outdated
- You want to refresh the index

---

## Using the Command Line

### Starting CLI Mode

```bash
python main.py
```

### Interacting with the Bot

```
Ask something (or type 'exit'): What is Docker?

Retrieved Context:
[Document chunks will be displayed here]

Gemini Answer:
[AI-generated answer will appear here]

Ask something (or type 'exit'): 
```

### Exiting CLI Mode

Type `exit` and press Enter.

### CLI Advantages

- No browser required
- Faster for quick queries
- Shows retrieved context directly
- Good for scripting and automation

---

## Managing Documents

### Supported File Types

| Format | Extension | Best For |
|--------|-----------|----------|
| Text | `.txt` | Plain documentation, notes |
| Markdown | `.md` | Technical docs, README files |
| CSV | `.csv` | Structured data, tables |
| PDF | `.pdf` | Reports, papers, books |
| Word | `.docx` | Business documents |

### Document Organization

**Best Practices:**

1. **Use descriptive filenames**
   - ✅ `kubernetes-deployment-guide.txt`
   - ❌ `doc1.txt`

2. **Keep documents focused**
   - One topic per document works best
   - Break large documents into sections

3. **Use clear formatting**
   - Use headings and sections
   - Keep paragraphs concise
   - Use bullet points for lists

4. **Avoid duplicate content**
   - Remove redundant documents
   - Merge similar content

### Adding Documents

**Method 1: Web Upload**
- Use the upload button in the web interface
- Automatic reindexing

**Method 2: Manual Copy**
1. Copy files to the `data/` folder
2. Click "Reindex" in the web interface
3. Or restart the application

### Removing Documents

1. Delete the file from the `data/` folder
2. Click "Reindex" in the web interface
3. The document will no longer be searchable

### Viewing Chat History

All conversations are saved to `data/history/chat_history.txt`

You can:
- Review past conversations
- Export for analysis
- Share with team members
- Use for training purposes

---

## Tips for Better Results

### Writing Effective Questions

**Be Specific**
- ❌ "Tell me about containers"
- ✅ "What are the main benefits of using Docker containers?"

**Provide Context**
- ❌ "How do I deploy?"
- ✅ "How do I deploy a Python Flask application to Kubernetes?"

**Ask One Thing at a Time**
- ❌ "What is Docker and how do I use it and what are containers?"
- ✅ "What is Docker?" (then follow up with more questions)

**Use Natural Language**
- ✅ "How can I scale my application?"
- ✅ "What's the difference between pods and deployments?"

### Improving Document Quality

**1. Structure Your Documents**
```markdown
# Main Topic

## Subtopic 1
Clear explanation here...

## Subtopic 2
More details here...
```

**2. Use Clear Language**
- Avoid jargon when possible
- Define technical terms
- Use examples

**3. Keep Content Current**
- Update documents regularly
- Remove outdated information
- Add new learnings

**4. Include Examples**
```
Good: "To create a pod, use: kubectl create pod my-pod"
Better: "To create a pod, use: kubectl create pod my-pod --image=nginx"
```

### Optimizing Performance

**For Faster Responses:**
- Use lower Top-K values (2-3)
- Keep documents concise
- Remove unnecessary files

**For Better Accuracy:**
- Use higher Top-K values (4-6)
- Add more relevant documents
- Improve document quality

**For Large Document Collections:**
- Organize by topic
- Use descriptive filenames
- Regular reindexing

---

## Common Questions

### Q: How many documents can I upload?

**A:** There's no hard limit, but performance may degrade with thousands of documents. For best results, keep your collection focused and relevant.

### Q: Can I use documents in other languages?

**A:** The system works best with English documents. Other languages may work but with reduced accuracy.

### Q: How accurate are the answers?

**A:** Accuracy depends on:
- Quality of your documents
- Relevance of retrieved context
- Clarity of your question
- The AI model's capabilities

Always verify important information!

### Q: Can I use this offline?

**A:** Partially. The document retrieval works offline, but you need internet access for the Gemini API to generate answers.

### Q: Is my data private?

**A:** Your documents stay on your machine. However, queries and context are sent to Google's Gemini API. Don't upload sensitive information without proper security measures.

### Q: Can I customize the AI's responses?

**A:** Yes! Edit the `ask_gemini()` function in `main.py` to modify the prompt template.

### Q: What if the bot gives wrong answers?

**A:** 
1. Check if relevant documents are uploaded
2. Verify document content is accurate
3. Try rephrasing your question
4. Increase Top-K to get more context
5. Review the retrieved context to see what the AI is working with

### Q: Can I integrate this with other applications?

**A:** Yes! See the API documentation for integration examples.

---

## Troubleshooting

### Problem: No answer or error message

**Solutions:**
1. Check if documents are uploaded
2. Verify API key is valid
3. Check internet connection
4. Look at the status message for details
5. Check browser console for errors (F12)

### Problem: Irrelevant answers

**Solutions:**
1. Rephrase your question more specifically
2. Check if relevant documents exist
3. Increase Top-K value
4. Review document content quality
5. Try reindexing

### Problem: Slow responses

**Solutions:**
1. Reduce Top-K value
2. Check internet speed
3. Reduce document collection size
4. Close other applications
5. Check server logs for issues

### Problem: Upload fails

**Solutions:**
1. Check file format is supported
2. Verify file isn't corrupted
3. Check file size (very large files may fail)
4. Try a different file
5. Check disk space

### Problem: Robot keeps thinking

**Solutions:**
1. Refresh the page
2. Check browser console for errors
3. Verify server is running
4. Check API key and internet connection
5. Restart the application

### Problem: Context shows wrong documents

**Solutions:**
1. Click "Reindex" to rebuild the index
2. Check for duplicate content
3. Improve document organization
4. Use more specific questions
5. Review document filenames

---

## Advanced Usage

### Custom Prompts

Edit the prompt in `main.py`:

```python
def ask_gemini(context, question):
    prompt = f"""You are a helpful assistant. Use the context below to answer questions.

Context:
{context}

Question: {question}
Answer:"""
    # ... rest of function
```

### Batch Processing

Process multiple questions:

```python
questions = [
    "What is Kubernetes?",
    "How do I deploy an app?",
    "What are pods?"
]

for q in questions:
    response = client.query(q)
    print(f"Q: {q}")
    print(f"A: {response['answer']}\n")
```

### Monitoring Usage

Check chat history:
```bash
tail -f data/history/chat_history.txt
```

### Backup Your Data

```bash
# Backup documents
tar -czf documents-backup.tar.gz data/

# Backup chat history
cp data/history/chat_history.txt chat_history_backup.txt
```

---

## Getting Help

### Resources

1. **README.md** - Installation and setup
2. **API_DOCUMENTATION.md** - API reference
3. **This Guide** - Usage instructions
4. **Code Comments** - In-line documentation

### Support Checklist

Before asking for help:
- [ ] Read this guide
- [ ] Check troubleshooting section
- [ ] Review error messages
- [ ] Try restarting the application
- [ ] Check the chat history for clues

### Reporting Issues

When reporting problems, include:
1. What you were trying to do
2. What happened instead
3. Error messages (if any)
4. Steps to reproduce
5. Your environment (OS, Python version)

---

## Best Practices Summary

✅ **DO:**
- Upload relevant, high-quality documents
- Ask clear, specific questions
- Review retrieved context
- Keep documents organized
- Reindex after bulk changes
- Verify important information

❌ **DON'T:**
- Upload sensitive data without security measures
- Ask overly broad questions
- Ignore error messages
- Upload duplicate content
- Forget to reindex after manual file additions
- Trust answers blindly

---

## Quick Reference

### Keyboard Shortcuts (Web Interface)
- `Enter` - Send message
- `Ctrl+R` - Refresh page
- `F12` - Open developer console

### Common Commands (CLI)
- `exit` - Quit the application
- `Ctrl+C` - Force quit

### File Locations
- Documents: `data/`
- Chat History: `data/history/chat_history.txt`
- Templates: `templates/`
- Styles: `static/css/styles.css`

---

## Conclusion

You're now ready to make the most of your RAG Chatbot! Remember:

1. **Start simple** - Upload a few documents and ask basic questions
2. **Experiment** - Try different Top-K values and question styles
3. **Iterate** - Improve your documents based on results
4. **Have fun** - Explore what your chatbot can do!

Happy chatting! 🤖💬

---

**Need more help?** Check out:
- README.md for technical details
- API_DOCUMENTATION.md for integration
- Code comments for implementation details

**Version:** 1.0  
**Last Updated:** November 2025
