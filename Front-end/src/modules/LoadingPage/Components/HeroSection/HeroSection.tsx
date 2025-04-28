import { Button, Container, Text, Title } from '@mantine/core';
import { Dots } from './Dots';
import classes from './HeroSection.module.css';

export function HeroText() {
  return (
    <Container className={classes.wrapper} size={1400}>
        <Dots className={classes.dots} style={{ left: 0, top: 0 }} />
        <Dots className={classes.dots} style={{ left: 60, top: 0 }} />
        <Dots className={classes.dots} style={{ left: 0, top: 140 }} />
        <Dots className={classes.dots} style={{ right: 0, top: 60 }} />

        <div className={classes.inner}>
            <Title className={classes.title}>
                Optimisez votre{' '}
                <Text component="span" className={classes.highlight} inherit>
                irrigation agricole 
                </Text>{' '}
                avec notre système intelligent
            </Title>

            <Container p={0} size={600}>
                <Text size="lg" c="dimmed" className={classes.description}>
                    Développé dans le cadre du module Systèmes Répartis & Distribués à 
                    <span className="font-bold">  l'Université Ibn Zohr</span>, 
                    notre projet vise à automatiser et optimiser l'irrigation des fermes grâce à des technologies 
                    distribuées avancées.
                </Text>
            </Container>

            <div className={classes.controls}>
                <Button className={classes.control} size="lg" variant="default" color="gray">
                    Notre solution
                </Button>
            </div>
        </div>
    </Container>
  );
}