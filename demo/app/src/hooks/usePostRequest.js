import { useEffect, useState } from "react";

const usePostRequest = (params) => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (params) {
            console.log('-------------------------------------------------')
            setIsLoading(true);
            fetch("/api/opportunities", {
                method: "POST",
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify({
                    ...params,
                    product_id: 'sentinel-2-l1c'
                })
            })
            .then((res) => res.json())
            .then((data) => {
                console.log('-------------------------------------------------')
                console.log("Data:", data)
                console.log("Data features:", data.features)
                setData(data.features)
                setIsLoading(false)
            }).catch((e) => {
                setError(e);
                setIsLoading(false);
            });
        }
    }, [params]);

    return { data, isLoading, error };
};

export default usePostRequest;
