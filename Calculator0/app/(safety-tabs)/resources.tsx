import { StyleSheet, ScrollView, Linking, Pressable } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';

export default function Resources() {
  const openLink = (url: string) => {
    Linking.openURL(url);
  };

  return (
    <ScrollView style={styles.container}>
      <ThemedView style={styles.content}>
        <ThemedText type="title" style={styles.title}>Resources</ThemedText>
        
        <ThemedText style={styles.blurb}>
          If you suspect that you are in an abusive relationship, please know that help is available. 
          You are not alone, and there are resources available to support you.
        </ThemedText>

        <ThemedView style={styles.resourceContainer}>
          <ThemedText type="subtitle" style={styles.resourceTitle}>
            National Domestic Violence Hotline
          </ThemedText>
          <Pressable onPress={() => openLink('tel:18007997233')}>
            <ThemedText style={styles.link}>1-800-799-7233</ThemedText>
          </Pressable>
          <ThemedText style={styles.description}>
            24/7 confidential support. Available in English, Spanish and 200+ through interpretation services.
          </ThemedText>
        </ThemedView>

        <ThemedView style={styles.resourceContainer}>
          <ThemedText type="subtitle" style={styles.resourceTitle}>
            Crisis Text Line
          </ThemedText>
          <ThemedText style={styles.description}>
            Text HOME to <ThemedText style={styles.link}>741741</ThemedText>
          </ThemedText>
          <ThemedText style={styles.description}>
            Free 24/7 crisis support via text message.
          </ThemedText>
        </ThemedView>

        <ThemedView style={styles.resourceContainer}>
          <ThemedText type="subtitle" style={styles.resourceTitle}>
            Online Resources
          </ThemedText>
          <Pressable onPress={() => openLink('https://www.thehotline.org')}>
            <ThemedText style={styles.link}>TheHotline.org</ThemedText>
          </Pressable>
          <Pressable onPress={() => openLink('https://www.loveisrespect.org')}>
            <ThemedText style={styles.link}>LoveIsRespect.org</ThemedText>
          </Pressable>
        </ThemedView>

        <ThemedText style={styles.emergency}>
          In an emergency, call 911
        </ThemedText>
      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    padding: 20,
  },
  title: {
    marginBottom: 20,
  },
  blurb: {
    fontSize: 16,
    marginBottom: 30,
    lineHeight: 24,
  },
  resourceContainer: {
    marginBottom: 25,
    padding: 15,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  resourceTitle: {
    marginBottom: 8,
  },
  link: {
    color: '#0a7ea4',
    fontSize: 16,
    marginVertical: 4,
    textDecorationLine: 'underline',
  },
  description: {
    fontSize: 14,
    marginTop: 8,
    lineHeight: 20,
  },
  emergency: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 20,
    color: '#dc2626',
  },
});