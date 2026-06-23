import { useState } from "react";
import api from "../api/medpatapi";

function UploadForm({setReportData} ){
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleUpload = async() =>{
        if(!file){
            alert("Please select a file");
            return;
        }
        
        const formData = new FormData()

        formData.append("file", file);


        try {
            setLoading(true);

            const response = await api.post(
                "/reports", 
                formData
            );

            console.log(response.data);

            setReportData(response.data);

            alert("Upload successful");     
            
        } catch (error) {
            console.log(error);

            alert("Upload failed");
            
        } finally {
             setLoading(false);
        }
        
    };

    return (
        <div>
            <h2> Upload Report </h2>

            <input type ="file"
            onChange={(e) => setFile(e.target.files[0])}
            />

            <button onClick={handleUpload}
            disabled={loading}
            >
               {
               loading?"Uploading...": "Upload"
               }
            </button>
        </div>
    )
}

export default UploadForm;