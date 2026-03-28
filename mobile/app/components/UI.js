import React from "react";
import { Pressable, StyleSheet, Text, TextInput, View } from "react-native";

export function Card({ children }) {
  return <View style={styles.card}>{children}</View>;
}

export function Heading({ children }) {
  return <Text style={styles.heading}>{children}</Text>;
}

export function Label({ children }) {
  return <Text style={styles.label}>{children}</Text>;
}

export function Input(props) {
  return <TextInput placeholderTextColor="#6a6a6a" style={styles.input} {...props} />;
}

export function Button({ title, onPress, variant = "primary" }) {
  return (
    <Pressable onPress={onPress} style={[styles.button, variant === "secondary" && styles.buttonSecondary]}>
      <Text style={[styles.buttonText, variant === "secondary" && styles.buttonSecondaryText]}>{title}</Text>
    </Pressable>
  );
}

export function Stat({ label, value }) {
  return (
    <View style={styles.stat}>
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={styles.statValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fffdf9",
    borderRadius: 18,
    padding: 16,
    gap: 10,
    borderWidth: 1,
    borderColor: "#e8dcc6"
  },
  heading: {
    fontSize: 26,
    fontWeight: "700",
    color: "#173a63"
  },
  label: {
    color: "#173a63",
    fontWeight: "600"
  },
  input: {
    borderWidth: 1,
    borderColor: "#d6c7af",
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 12,
    backgroundColor: "#ffffff"
  },
  button: {
    backgroundColor: "#173a63",
    padding: 14,
    borderRadius: 14,
    alignItems: "center"
  },
  buttonSecondary: {
    backgroundColor: "#efe4d0"
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "700"
  },
  buttonSecondaryText: {
    color: "#173a63"
  },
  stat: {
    padding: 14,
    borderRadius: 16,
    backgroundColor: "#efe4d0",
    gap: 4
  },
  statLabel: {
    color: "#6a5d49"
  },
  statValue: {
    color: "#173a63",
    fontSize: 22,
    fontWeight: "700"
  }
});
