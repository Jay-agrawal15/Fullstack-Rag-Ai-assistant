import React, { useState } from "react";
import "./App.css";

function App() {

  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const askQuestion = async () => {

    if (!question.trim()) return;

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();

      setResult(data);

      setHistory((prev) => [
        question,
        ...prev,
      ]);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  const clearChat = () => {
    setResult(null);
    setQuestion("");
  };

  const handleKeyDown = (e) => {

    if (e.key === "Enter") {
      askQuestion();
    }
  };

  return (
    <div className="app">

      {/* SIDEBAR */}

      <div className="sidebar">

        <h2>Previous Chats</h2>

        {
          history.map((item, index) => (
            <div
              key={index}
              className="history-item"
            >
              {item}
            </div>
          ))
        }

        <button
          className="clear-btn"
          onClick={clearChat}
        >
          Clear Chat
        </button>

      </div>

      {/* MAIN */}

      <div className="main">

        <h1>
          Welcome to Jay's AI Tech Knowledge Assistant
        </h1>

        <p className="subtitle">
          This project is an advanced AI-powered
          RAG (Retrieval-Augmented Generation)
          assistant built using FastAPI, React,
          LangChain, FAISS, Hybrid Search,
          Reranking, and Local LLMs.
        </p>

        {/* INPUT */}

        <div className="search-box">

          <input
            type="text"
            placeholder="Ask any AI or Machine Learning question..."
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            onKeyDown={handleKeyDown}
          />

          <button onClick={askQuestion}>
            Ask
          </button>

        </div>

        {/* LOADING */}

        {
          loading && (
            <div className="thinking">
              AI is thinking...
            </div>
          )
        }

        {/* RESULT */}

        {
          result && !loading && (
            <div className="result-box">

              <h2>Answer</h2>

              <p>{result.answer}</p>

              <div className="metrics">

                <div className="metric-card">
                  <h3>Confidence</h3>
                  <p>{result.confidence}</p>
                </div>

                <div className="metric-card">
                  <h3>Latency</h3>
                  <p>{result.latency} sec</p>
                </div>

              </div>

              <h3>Sources</h3>

              <ul>

                {
                  result.sources &&
                  result.sources.map(
                    (source, index) => (
                      <li key={index}>
                        {source}
                      </li>
                    )
                  )
                }

              </ul>

            </div>
          )
        }

      </div>

    </div>
  );
}

export default App;