import { HeaderMegaMenu } from "./Components/NavBar/Header"
import { HeroText } from "./Components/HeroSection/HeroSection"
import { SolutionFeatures } from "./Components/SolutionSection/Solution"
import { TechSection } from "./Components/TechSection/TechSection"

const Home = () => {
  return (
    <>
      <HeaderMegaMenu />
      <HeroText />
      <SolutionFeatures />
      <TechSection />
    </>
  )
}

export default Home