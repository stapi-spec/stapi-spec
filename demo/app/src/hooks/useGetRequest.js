import { useEffect, useState } from "react";

const useGetRequest = () => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        fetch('/api/products')
        .then((res) => res.json())
        .then((data) => {
            setData(data['products'])
            setIsLoading(false)
        }).catch(e => setError(e));
    }, []);

    return { data, isLoading, error };
};

export default useGetRequest;
