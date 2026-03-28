import AsyncStorage from "@react-native-async-storage/async-storage";
import React, { createContext, useContext, useEffect, useState } from "react";

import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const restore = async () => {
      const storedToken = await AsyncStorage.getItem("token");
      if (storedToken) {
        setToken(storedToken);
        try {
          const currentUser = await api.me(storedToken);
          setUser(currentUser);
        } catch {
          await AsyncStorage.removeItem("token");
          setToken(null);
        }
      }
      setLoading(false);
    };
    restore();
  }, []);

  const authenticate = async (method, payload) => {
    const data = method === "signup" ? await api.signup(payload) : await api.login(payload);
    await AsyncStorage.setItem("token", data.access_token);
    setToken(data.access_token);
    const currentUser = await api.me(data.access_token);
    setUser(currentUser);
  };

  const logout = async () => {
    await AsyncStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, setUser, loading, authenticate, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
