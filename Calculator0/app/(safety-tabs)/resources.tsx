// import { StyleSheet, ScrollView, Linking, Pressable } from 'react-native';
// import { ThemedText } from '@/components/themed-text';
// import { ThemedView } from '@/components/themed-view';

// export default function Resources() {
//   const openLink = (url: string) => {
//     Linking.openURL(url);
//   };

//   return (
//     <ScrollView style={styles.container}>
//       <ThemedView style={styles.content}>
//         <ThemedText type="title" style={styles.title}>Resources</ThemedText>
        
//         <ThemedText style={styles.blurb}>
//           If you suspect that you are in an abusive relationship, please know that help is available. 
//           You are not alone, and there are resources available to support you.
//         </ThemedText>

//         <ThemedView style={styles.resourceContainer}>
//           <ThemedText type="subtitle" style={styles.resourceTitle}>
//             National Domestic Violence Hotline
//           </ThemedText>
//           <Pressable onPress={() => openLink('tel:18007997233')}>
//             <ThemedText style={styles.link}>1-800-799-7233</ThemedText>
//           </Pressable>
//           <ThemedText style={styles.description}>
//             24/7 confidential support. Available in English, Spanish and 200+ through interpretation services.
//           </ThemedText>
//         </ThemedView>

//         <ThemedView style={styles.resourceContainer}>
//           <ThemedText type="subtitle" style={styles.resourceTitle}>
//             Crisis Text Line
//           </ThemedText>
//           <ThemedText style={styles.description}>
//             Text HOME to <ThemedText style={styles.link}>741741</ThemedText>
//           </ThemedText>
//           <ThemedText style={styles.description}>
//             Free 24/7 crisis support via text message.
//           </ThemedText>
//         </ThemedView>

//         <ThemedView style={styles.resourceContainer}>
//           <ThemedText type="subtitle" style={styles.resourceTitle}>
//             Online Resources
//           </ThemedText>
//           <Pressable onPress={() => openLink('https://www.thehotline.org')}>
//             <ThemedText style={styles.link}>TheHotline.org</ThemedText>
//           </Pressable>
//           <Pressable onPress={() => openLink('https://www.loveisrespect.org')}>
//             <ThemedText style={styles.link}>LoveIsRespect.org</ThemedText>
//           </Pressable>
//         </ThemedView>

//         <ThemedText style={styles.emergency}>
//           In an emergency, call 911
//         </ThemedText>
//       </ThemedView>
//     </ScrollView>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     backgroundColor: "#242e24",
//   },
//   content: {
//     padding: 20,
//   },
//   title: {
//     marginBottom: 20,
//     color:'#242e24',
//   },
//   blurb: {
//     fontSize: 16,
//     marginBottom: 30,
//     lineHeight: 24,
//   },
//   resourceContainer: {
//     marginBottom: 25,
//     padding: 15,
//     borderRadius: 8,
//     borderWidth: 1,
//     borderColor: '#ddd',
//   },
//   resourceTitle: {
//     marginBottom: 8,
//   },
//   link: {
//     color: '#0a7ea4',
//     fontSize: 16,
//     marginVertical: 4,
//     textDecorationLine: 'underline',
//   },
//   description: {
//     fontSize: 14,
//     marginTop: 8,
//     lineHeight: 20,
    
//   },
  
//   emergency: {
//     fontSize: 18,
//     fontWeight: 'bold',
//     textAlign: 'center',
//     marginTop: 20,
//     color: '#dc2626',
//   },
// });

import { StyleSheet, ScrollView, Linking, Pressable, View, SafeAreaView } from 'react-native';
import { ThemedText } from '@/components/themed-text';

export default function Resources() {
  const openLink = (url: string) => {
    Linking.openURL(url);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView 
        style={styles.container}
        contentContainerStyle={styles.scrollContent}
      >
        <View style={styles.content}>
          <ThemedText type="title" style={styles.title}>Resources</ThemedText>
          
          <ThemedText style={styles.blurb}>
            If you suspect that you are in an abusive relationship, please know that help is available. 
            You are not alone, and there are resources available to support you.
          </ThemedText>

          <View style={styles.resourceContainer}>
            <ThemedText type="subtitle" style={styles.resourceTitle}>
              National Domestic Violence Hotline
            </ThemedText>
            <Pressable onPress={() => openLink('tel:18007997233')}>
              <ThemedText style={styles.link}>1-800-799-7233</ThemedText>
            </Pressable>
            <ThemedText style={styles.description}>
              24/7 confidential support. Available in English, Spanish and 200+ through interpretation services.
            </ThemedText>
          </View>

          <View style={styles.resourceContainer}>
            <ThemedText type="subtitle" style={styles.resourceTitle}>
              Crisis Text Line
            </ThemedText>
            <ThemedText style={styles.description}>
              Text HOME to <ThemedText style={styles.link}>741741</ThemedText>
            </ThemedText>
            <ThemedText style={styles.description}>
              Free 24/7 crisis support via text message.
            </ThemedText>
          </View>

          <View style={styles.resourceContainer}>
            <ThemedText type="subtitle" style={styles.resourceTitle}>
              Online Resources
            </ThemedText>
            <Pressable onPress={() => openLink('https://www.thehotline.org')}>
              <ThemedText style={styles.link}>TheHotline.org</ThemedText>
            </Pressable>
            <Pressable onPress={() => openLink('https://www.loveisrespect.org')}>
              <ThemedText style={styles.link}>LoveIsRespect.org</ThemedText>
            </Pressable>
          </View>

          <ThemedText style={styles.emergency}>
            In an emergency, call 911
          </ThemedText>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#242e24', // Dark green background
  },
  container: {
    flex: 1,
    backgroundColor: '#242e24', // Dark green background
  },
  scrollContent: {
    flexGrow: 1,
  },
  content: {
    padding: 20,
  },
  title: {
    marginBottom: 20,
    color: '#ecfad4', // White title
  },
  blurb: {
    fontSize: 16,
    marginBottom: 30,
    lineHeight: 24,
    color: '#E0E0E0', // Light gray text
  },
  resourceContainer: {
    marginBottom: 25,
    padding: 15,
    borderRadius: 8,
    backgroundColor: '#3d4f3d', 
    borderWidth: 1,
    borderColor: '#2D6B4F', // Green border
  },
  resourceTitle: {
    marginBottom: 8,
    color: '#ecfad4',
  },
  link: {
    color: '#40c251', // Teal/cyan for links (better contrast on dark green)
    fontSize: 16,
    marginVertical: 4,
    textDecorationLine: 'underline',
  },
  description: {
    fontSize: 14,
    marginTop: 8,
    lineHeight: 20,
    color: '#B0B0B0', // Medium gray text
  },
  emergency: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 30,
    color: '#FF6B6B', // Softer red that works on dark green
  },
});