import { Cpu, Wifi, Database, Code2, Monitor } from 'lucide-react';
import { Container, Grid, Text, Title } from '@mantine/core';
import classes from './TechSection.module.css';

interface TechnologyProps {
  icon: React.ComponentType<any>;
  title: string;
  description: string;
}

function Technology({ icon: Icon, title, description }: TechnologyProps) {
  return (
    <div className={classes.technology}>
        <div className={classes.iconWrapper}>
            <div className={classes.icon}>
                <Icon size={32} />
            </div>
        </div>
        <div className={classes.content}>
            <Text fw={700} fz="lg" className={classes.title} ta="center">
                {title}
            </Text>
            <Text c="dimmed" fz="sm" ta="center">
                {description}
            </Text>
        </div>
    </div>
  );
}

const technologies = [
  {
    icon: Cpu,
    title: 'Microcontrôleur',
    description: 'Arduino/ESP32',
  },
  {
    icon: Wifi,
    title: 'Communication',
    description: 'CORBA (omniORB)',
  },
  {
    icon: Database,
    title: 'Base de données',
    description: 'MySQL/SQLite',
  },
  {
    icon: Code2,
    title: 'Backend',
    description: 'Flask (Python)',
  },
  {
    icon: Monitor,
    title: 'Interface Web',
    description: 'React.JS',
  },
];

export function TechSection() {
  return (
    <Container  py={40} className={classes.section}>
        <Title order={2} className={classes.sectionTitle} ta="center" mb={30}>
            Technologies Utilisées
        </Title>
        
        <Grid 
            justify="center"
            gutter="xl"
            styles={{
                inner: {
                    justifyContent: 'center',
                }
            }}
        >
            {technologies.map((tech, index) => (
                <Grid.Col 
                    key={index}
                    span={{ base: 12, sm: 6, md: 4 }}  
                >
                    <Technology 
                        icon={tech.icon}
                        title={tech.title}
                        description={tech.description}
                    />
                </Grid.Col>
            ))}
        </Grid>
    </Container>
  );
}