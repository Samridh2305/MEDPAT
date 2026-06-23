import { useState } from "react";
import api from "../api/medpatapi";

function PredictionForm({
  reportId,
  setPrediction
}) {

  const [loading, setLoading] = useState(false);

  const handlePrediction = async () => {
    try {
      if (!reportId) {
        alert("Upload a report first");
        return;
      }   

      setLoading(true);
      setPrediction(null);

      const response = await api.post(
        `/reports/${reportId}/predict`
      );

      setPrediction(response.data);

    } catch (error) {

      console.log(error);
      alert("Prediction failed");

    } finally {
      setLoading(false);

    }
  };

  return (
    <div>
      <button onClick={handlePrediction}
      disabled={loading}>
        {loading?"Predicting...":"Predict Diseases"}
      </button>
    </div>
  );
}

export default PredictionForm;