/** Base HTTP API Client with graceful fallback to mock data when offline. */

const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error ${response.status}: ${response.statusText}`);
    }

    return (await response.json()) as T;
  } catch (error) {
    console.warn(`Backend API unreachable at ${url}. Falling back to client-side data.`, error);
    throw error;
  }
}
