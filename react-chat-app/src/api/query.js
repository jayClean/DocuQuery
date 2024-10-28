// src/api/query.js
import axiosInstance from './axiosConfig';

// Example of querying the API from your React component
export const queryDocuments = async (queryText) => {
    try {
        const response = await axiosInstance.get(`/search`,  {
            params: { query: queryText },  // Attach queryText as a query parameter  // Send the query in the request body
        }, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`  // Ensure token is defined
            }
        });
        console.log(response.data); // Handle the response data
        return response.data
    } catch (error) {
        console.error("Error querying documents:", error);
        alert("Failed to query documents.");
    }
};
