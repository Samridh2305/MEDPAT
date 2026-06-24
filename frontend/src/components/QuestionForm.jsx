import { useState } from "react";
import api from "../api/medpatapi";
import ReactMarkdown from "react-markdown";

function QuestionForm({reportId}){
    const [question, setQuestion] = useState("");
    const [answer, setAnswer]= useState("");
    const [loading, setLoading] = useState(false);

    const handleQuestion = async() =>{

      if (!question.trim()) {
      alert("Please enter a question");
      return;
      }

      try{
        setAnswer("");
        setLoading(true);
        const response = await api.post(
            "/questions", 
            {
                report_id: reportId,
                question: question
            }
        );

        setAnswer(response.data.answer);   

      } catch(error){
        console.log(error)
        alert("Sorry, Unable to answer the question")

      } finally {
        setLoading(false);

      }                   
    };

return (
    <div>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={handleQuestion}
      disabled={loading}
      >
        {
        loading? "Asking...":"Ask"
        }
      </button>

      <div className="answer-box">
        <ReactMarkdown>
          {answer}
        </ReactMarkdown>
      </div>

    </div>
  );
}

export default QuestionForm;