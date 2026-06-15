import OpenAI from '../assets/OpenAI.svg'
import Anthropic from '../assets/Anthropic.svg'
import Google from '../assets/Google.svg'
import Meta from '../assets/Meta.svg'
import DeepSeek from '../assets/DeepSeek.svg'
import XAI from '../assets/XAI.svg'
import MiniMax from '../assets/minimax.svg'
import logo from '../assets/logo.svg'

export const companyLogos = {
  OpenAI,
  Anthropic,
  Google,
  Meta,
  DeepSeek,
  XAI,
  MiniMax,
  logo
}

export function useCompanyLogos() {
  const formatCompany = (company) => {
    const logo = companyLogos[company]
    if (logo) {
      return `<img src="${logo}" alt="${company}" class="h-5 inline-block mr-1" /> ${company}`
    }
    return company
  }
  const getCompanyLogo = (company) => {
    return companyLogos[company]
  }

  return {
    companyLogos,
    formatCompany,
    getCompanyLogo
  }
}