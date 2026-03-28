import React from "react";
import { ActivityIndicator, View } from "react-native";
import { NavigationContainer } from "@react-navigation/native";

import { AuthProvider, useAuth } from "./app/context/AuthContext";
import { AuthStack } from "./app/screens/AuthStack";
import { MainTabs } from "./app/screens/MainTabs";

function RootNavigator() {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: "#f4f1ea" }}>
        <ActivityIndicator size="large" color="#173a63" />
      </View>
    );
  }

  return <NavigationContainer>{token ? <MainTabs /> : <AuthStack />}</NavigationContainer>;
}

export default function App() {
  return (
    <AuthProvider>
      <RootNavigator />
    </AuthProvider>
  );
}
