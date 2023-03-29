import { useEffect, useState } from "react";

const useApiRequest = (params) => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (params) {
            setIsLoading(true);
            fetch("/api/pineapple", {
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
                // expect list once complete
                if(typeof data === 'object'){
                    data = [data]
                }
                setData(data)
                setIsLoading(false)
            }).catch(e => setError(e));
        }
    }, [params]);
    
    return { data, isLoading, error };
};
    
export default useApiRequest;
