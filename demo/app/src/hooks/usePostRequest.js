import { useEffect, useState } from "react";

const usePostRequest = (params) => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (params) {
            setIsLoading(true);
            fetch("/api/opportunities", {
                method: "POST",
                headers: {
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

export default usePostRequest;
