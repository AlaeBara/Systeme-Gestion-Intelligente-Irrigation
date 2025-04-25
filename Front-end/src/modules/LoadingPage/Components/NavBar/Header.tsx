import {
    Box,
    Burger,
    Button,
    Divider,
    Drawer,
    Group,
    ScrollArea,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import classes from './Header.module.css';
import logo from './logo.png'
  
 
export function HeaderMegaMenu() {
    const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] = useDisclosure(false);
  
    return (
        <Box pb={120}>
            <header className={classes.header}>
                <Group justify="space-between" h="100%">

                    <img src={logo} alt="logo" width={100} height={100}  />
        
                    <Group h="100%" gap={0} visibleFrom="md">
                        <a href="#" className={classes.link}>
                            Accueil
                        </a>
                        
                        <a href="#" className={classes.link}>
                            Notre solution
                        </a>
                        <a href="#" className={classes.link}>
                            Équipe du Projet
                        </a>

                        <a href="#" className={classes.link}>
                            Technologies Utilisées  
                        </a>

                        <a href="#" className={classes.link}>
                            Perspectives Futures
                        </a>
                        
                    </Group>
        
                    <Group visibleFrom="md">
                        <Button variant="default">Log in</Button>
                    </Group>
        
                    <Burger opened={drawerOpened} onClick={toggleDrawer} hiddenFrom="md" />
                </Group>
            </header>
    
            <Drawer
                opened={drawerOpened}
                onClose={closeDrawer}
                size="100%"
                padding="md"
                title='SmartIrrigation'
                hiddenFrom="md"
                zIndex={1000000}
            >
                <ScrollArea h="calc(100vh - 80px)" mx="-md">
                    <Divider my="sm" />

                    <a href="#" className={classes.link}>
                        Accueil
                    </a>
            
                    <a href="#" className={classes.link}>
                        Notre solution
                    </a>

                    <a href="#" className={classes.link}>
                        Équipe du Projet
                    </a>

                    <a href="#" className={classes.link}>
                        Technologies Utilisées
                    </a>

                    <a href="#" className={classes.link}>
                        Perspectives Futures
                    </a>
        
                    <Divider my="sm" />
        
                    <Group justify="center" grow pb="xl" px="md">
                        <Button variant="default">Log in</Button>
                    </Group>
                </ScrollArea>
            </Drawer>
        </Box>
    );
  }