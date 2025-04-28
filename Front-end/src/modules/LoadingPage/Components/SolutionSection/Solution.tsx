import { Container, SimpleGrid, Text, ThemeIcon, Title } from '@mantine/core';
import { Droplet, Wifi, Database, Cpu, Gauge, AlertCircle } from 'lucide-react';
import classes from './Solution.module.css';

const features = [
  {
    icon: Droplet,
    title: 'Capteurs Intelligents',
    description: 'Mesure précise de l\'humidité du sol en temps réel avec des capteurs connectés (Arduino/ESP32)',
  },
  {
    icon: Cpu,
    title: 'Microcontrôleur',
    description: 'Traitement local des données et activation automatique de la pompe lorsque l\'humidité < 30%',
  },
  {
    icon: Wifi,
    title: 'Communication CORBA',
    description: 'Architecture distribuée robuste avec omniORB pour une transmission fiable des données',
  },
  {
    icon: Database,
    title: 'Base de Données',
    description: 'Stockage sécurisé des historiques d\'irrigation dans une base MySQL pour analyse',
  },
  {
    icon: Gauge,
    title: 'Interface Web',
    description: 'Tableau de bord Flask pour visualisation et contrôle à distance du système',
  },
  {
    icon: AlertCircle,
    title: 'Alertes Intelligentes',
    description: 'Détection des anomalies et notifications pour intervention rapide',
  },
];

export function SolutionFeatures() {
    const items = features.map((feature) => (
      <div className={classes.item} key={feature.title}>
        <ThemeIcon variant="light" className={classes.itemIcon} size={60} radius="md">
          <feature.icon size={30} />
        </ThemeIcon>

        <div>
            <Text fw={700} fz="lg" className={classes.itemTitle}>
                {feature.title}
            </Text>
            <Text c="dimmed">{feature.description}</Text>
        </div>
      </div>
    ));

  return (
    <Container className={classes.wrapper} id="solution">
      <Text className={classes.supTitle}>
        Notre Solution Technique
      </Text>

      <Title className={classes.title} order={2}>
        Un système <span className={classes.highlight}>complet</span> pour une irrigation intelligente
      </Title>

      <Container size={660} p={0}>
        <Text c="dimmed" className={classes.description}>
          Notre architecture distribuée combine matériel embarqué et technologies serveur pour optimiser
          l'utilisation de l'eau. Chaque composant assure une fonction clé dans la chaîne d'irrigation automatisée.
        </Text>
      </Container>

      <SimpleGrid cols={{ base: 1, xs: 2, sm: 3 }} spacing={50} mt={30}>
        {items}
      </SimpleGrid>
    </Container>
  );
}