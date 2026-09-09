import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const API_TIMEOUT = Number(
  import.meta.env.VITE_API_TIMEOUT ?? 120000,
);

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    Accept: "application/json",
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      return Promise.reject(error);
    }

    if (error.request) {
      return Promise.reject(
        new Error(
          "Unable to connect to the RAG API. Make sure the FastAPI server is running.",
        ),
      );
    }

    return Promise.reject(error);
  },
);