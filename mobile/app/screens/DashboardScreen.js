import React, { useCallback, useState } from "react";
import { Alert, RefreshControl, Text, View } from "react-native";
import { useFocusEffect } from "@react-navigation/native";

import { api } from "../api/client";
import { Screen } from "../components/Screen";
import { Card, Heading, Stat } from "../components/UI";
import { useAuth } from "../context/AuthContext";

export function DashboardScreen() {
  const { token, user } = useAuth();
  const [data, setData] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    setRefreshing(true);
    try {
      setData(await api.dashboard(token));
    } catch (error) {
      Alert.alert("Could not load dashboard", error.message);
    } finally {
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      load();
    }, [token])
  );

  return (
    <Screen refreshControl={<RefreshControl refreshing={refreshing} onRefresh={load} />}>
      <Heading>{user?.full_name}</Heading>
      <View style={{ flexDirection: "row", gap: 12, flexWrap: "wrap" }}>
        <Stat label="Balance" value={`INR ${data?.balance ?? 0}`} />
        <Stat label="P&L" value={`INR ${data?.pnl ?? 0}`} />
        <Stat label="Trades" value={`${data?.total_trades ?? 0}`} />
        <Stat label="Win Rate" value={`${data?.win_rate ?? 0}%`} />
      </View>
      <Card>
        <Text style={{ fontWeight: "700", color: "#173a63" }}>Connected exchange</Text>
        <Text>{data?.connected_exchange || "Not connected"}</Text>
      </Card>
      <Card>
        <Text style={{ fontWeight: "700", color: "#173a63" }}>Portfolio snapshot</Text>
        {(data?.portfolio || []).slice(0, 6).map((item, index) => (
          <Text key={`${item.currency || "asset"}-${index}`}>
            {item.currency || item.symbol}: {item.main_balance || item.balance || "-"} | Current value: {item.current_value ?? "-"}
          </Text>
        ))}
      </Card>
    </Screen>
  );
}
