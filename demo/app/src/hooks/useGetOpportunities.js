import { useEffect, useState } from "react";
import useLocalStorage from "./useLocalStorage";

const useGetOpportunities = (postParams) => {
    const {params, provider} = !!postParams && postParams;
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const { userToken } = useLocalStorage();

    useEffect(() => {
        if (params) {
            setIsLoading(true);
            setError(false);
            fetch("/api/opportunities", {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                    "Backend": provider,
                    'Authorization': `Bearer ${userToken}`
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

export default useGetOpportunities;
