import { useEffect, useState } from "react";

const usePostRequest = (postParams) => {
    const {params, provider} = !!postParams && postParams;
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (params) {
            setIsLoading(true);
            fetch("/api/opportunities", {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                    "Backend": provider
                },
                body: JSON.stringify(params)
            })
            .then((res) => res.json())
            .then((data) => {
                setData(data.features)
                setIsLoading(false)
            }).catch(e => {
                setError(e);
                setIsLoading(false);
            });
        }
    }, [params, provider]);

    return { data, isLoading, error };
};

export default usePostRequest;
