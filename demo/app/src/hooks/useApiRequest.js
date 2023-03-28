import { useEffect, useState } from "react";

const useApiRequest = (params) => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        params && fetch("/api/pineapple", {
            method: "POST",
            headers: {
                "Authorization": "fake-token",
                "Backend": "fake",
                "Content-type": "application/json"
            },
            body: JSON.stringify(params)
        })
        .then((res) => res.json())
        .then((data) => {
            setData(data)
            setIsLoading(false)
        }).catch(e => setError(e));
    }, [params]);
    
    return { data, isLoading, error };
};
    
export default useApiRequest;
