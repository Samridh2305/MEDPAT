import "./App.css";
import { useState } from "react";
import UploadForm from "./components/UploadForm";
import QuestionForm from "./components/QuestionForm";
import PredictionForm from "./components/PredictionForm";

function App() {
  const [reportData, setReportData] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleReportUpload = (data) => {
    setReportData(data);
    setPrediction(null);
  };

  return (
    <div className="app-container">
      <h1 className="title">MEDPAT</h1>

      <UploadForm setReportData={handleReportUpload} />

      {reportData && (
        <div className="card">
          <h2>Uploaded Report</h2>

          <div className="report-info">
            <p>
              <strong>Report ID:</strong> {reportData.report_id}
            </p>

            <p>
              <strong>Filename:</strong> {reportData.filename}
            </p>
          </div>

          <h2>Extracted Lab Values</h2>

          <div className="labs-grid">
            {reportData.extracted_values?.map((lab, index) => (
              <div key={index} className="lab-card">
                <span className="lab-name">
                  {lab.normalized_name || lab.raw_name}
                </span>

                <span className="lab-value">
                  {lab.value} {lab.unit}
                </span>
              </div>
            ))}
          </div>

          <hr />

          <QuestionForm reportId={reportData.report_id} />

          <hr />

          <PredictionForm
            reportId={reportData.report_id}
            setPrediction={setPrediction}
          />

          {prediction && (
            <div className="prediction-card">
              <h2>Disease Prediction</h2>

              <div className="risk-item">
                <strong>Diabetes Risk</strong>
                <span>{prediction.diabetes_risk}%</span>
              </div>

              <div className="risk-item">
                <strong>Kidney Risk</strong>
                <span>{prediction.kidney_risk}%</span>
              </div>

              <div className="risk-item">
                <strong>Hypertension Risk</strong>
                <span>{prediction.hypertension_risk}%</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;