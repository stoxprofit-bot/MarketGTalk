import React from "react";
import { SafeAreaView, ScrollView, StyleSheet } from "react-native";

export function Screen({ children, refreshControl }) {
  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content} refreshControl={refreshControl}>
        {children}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: "#f4f1ea"
  },
  content: {
    padding: 20,
    gap: 16
  }
});
