import { Button } from '@/components/ui/button'
import { MapPin, Copy, Upload, Share2 } from 'lucide-react'
import { toast } from 'sonner'
import { formatResultsAsText, copyResultsToClipboard } from '@/lib/downloadUtils'
import type { AnalysisResult } from '@/types'

interface CTAActionsProps {
  tier: 'low' | 'moderate' | 'high'
  results: AnalysisResult
  onAnalyzeAnother?: () => void
}

const tierActions = {
  low: {
    primary: 'Learn More',
    url: 'https://www.aad.org/public/diseases/skin-cancer'
  },
  moderate: {
    primary: 'Find a Dermatologist',
    url: 'https://find-a-derm.aad.org/search?searchTerm=&searchLocation='
  },
  high: {
    primary: 'Find a Dermatologist',
    url: 'https://find-a-derm.aad.org/search?searchTerm=&searchLocation='
  }
}

export function CTAActions({ tier, results, onAnalyzeAnother }: CTAActionsProps) {
  const actions = tierActions[tier]

  const getZipCode = async (lat: number, lon: number): Promise<string | null> => {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=18&addressdetails=1`,
        { headers: { 'User-Agent': 'SkinTag-App' } }
      )
      const data = await response.json()
      return data.address?.postcode || null
    } catch {
      return null
    }
  }

  const handleClick = async (url: string) => {
    if (url.includes('find-a-derm.aad.org')) {
      try {
        const position = await new Promise<GeolocationPosition>((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 })
        })

        const zipCode = await getZipCode(position.coords.latitude, position.coords.longitude)
        if (zipCode) {
          window.open(url.replace('searchLocation=', `searchLocation=${zipCode}`), '_blank', 'noopener,noreferrer')
          return
        }
      } catch (error) {
        console.log('Location access denied or failed, using default location')
      }
    }

    window.open(url, '_blank', 'noopener,noreferrer')
  }

  const handleCopy = () => {
    try {
      const text = formatResultsAsText(results)
      copyResultsToClipboard(text)
      toast.success('Results copied to clipboard')
    } catch (error) {
      toast.error('Failed to copy to clipboard')
    }
  }

  const handleShare = () => {
    const text = formatResultsAsText(results)
    const shareData = {
      title: 'SkinTag Analysis Results',
      text: text,
    }

    if (navigator.share && navigator.canShare(shareData)) {
      navigator.share(shareData)
        .then(() => toast.success('Results shared'))
        .catch(() => {
          copyResultsToClipboard(text)
          toast.success('Results copied to clipboard')
        })
    } else {
      copyResultsToClipboard(text)
      toast.success('Results copied - ready to share with doctor')
    }
  }

  return (
    <div className="space-y-3">
      <Button
        onClick={() => handleClick(actions.url)}
        className="w-full"
        size="lg"
      >
        <MapPin className="w-5 h-5" />
        {actions.primary}
      </Button>

      <div className="grid grid-cols-2 gap-3">
        <Button
          onClick={handleShare}
          variant="outline"
          size="default"
        >
          <Share2 className="w-4 h-4" />
          Share
        </Button>
        <Button
          onClick={handleCopy}
          variant="outline"
          size="default"
        >
          <Copy className="w-4 h-4" />
          Copy
        </Button>
      </div>

      {onAnalyzeAnother && (
        <Button
          onClick={onAnalyzeAnother}
          variant="ghost"
          className="w-full"
        >
          <Upload className="w-4 h-4" />
          Analyze Another Image
        </Button>
      )}
    </div>
  )
}
