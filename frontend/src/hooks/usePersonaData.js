import { useState, useEffect, useRef } from 'react';
import { getPersonaDashboard } from '../api/client';

export function usePersonaData(personaId) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const cache = useRef({});

  useEffect(() => {
    if (!personaId || personaId === 'architecture' || personaId === 'speak_with_data') return;

    if (cache.current[personaId]) {
      setData(cache.current[personaId]);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    getPersonaDashboard(personaId)
      .then((result) => {
        cache.current[personaId] = result;
        setData(result);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [personaId]);

  return { data, loading, error };
}
