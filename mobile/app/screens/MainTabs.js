import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

import { AdminScreen } from "./AdminScreen";
import { DashboardScreen } from "./DashboardScreen";
import { SettingsScreen } from "./SettingsScreen";
import { TradesScreen } from "./TradesScreen";
import { useAuth } from "../context/AuthContext";

const Tab = createBottomTabNavigator();

export function MainTabs() {
  const { user } = useAuth();

  return (
    <Tab.Navigator screenOptions={{ headerStyle: { backgroundColor: "#173a63" }, headerTintColor: "#fff" }}>
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Trades" component={TradesScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
      {user?.role === "admin" ? <Tab.Screen name="Admin" component={AdminScreen} /> : null}
    </Tab.Navigator>
  );
}
