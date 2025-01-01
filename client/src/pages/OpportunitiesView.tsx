import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, ChevronRight, Sparkles } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

interface IdeaWithDetails {
  title: string;
  content: string;
  fullContent: string;
}

const IdeaCard = ({ idea }: { idea: IdeaWithDetails }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <Card className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <h4 className="font-bold mb-2">{idea.title}</h4>
      <p className="text-gray-700">
        {expanded ? idea.fullContent : idea.content}
      </p>
      {idea.fullContent !== idea.content && (
        <Button 
          variant="ghost" 
          onClick={() => setExpanded(!expanded)}
          className="text-blue-600 hover:text-blue-800 mt-2 p-0 h-auto"
        >
          {expanded ? 'Read less' : 'Read more'}
        </Button>
      )}
    </Card>
  );
};

interface OpportunityCardProps {
  title: string;
  description: string;
  ideas: IdeaWithDetails[];
  index: number;
}

const OpportunityCard: React.FC<OpportunityCardProps> = ({ title, description, ideas, index }) => {
  const [expanded, setExpanded] = useState(false);

  const getImage = (index: number) => {
    switch(index) {
      case 0: return '/api/placeholder/400/300'; // AI Matchmaker image
      case 1: return '/api/placeholder/400/300'; // Nonna's Pistachio image
      case 2: return '/api/placeholder/400/300'; // Berry Boost image
      case 3: return '/api/placeholder/400/300'; // Eco Packaging image
      default: return '/api/placeholder/400/300';
    }
  };

  return (
    <Card className="w-full mb-8 overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="flex flex-row">
        <div className="flex-1 p-6">
          <CardHeader className="p-0">
            <CardTitle className="text-2xl font-bold mb-4">{title}</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <p className="text-gray-600 mb-6">{description}</p>

            <div className="space-y-4">
              <div className="grid grid-cols-1 gap-3">
                {ideas.slice(0, expanded ? undefined : 3).map((idea, idx) => (
                  <IdeaCard key={idx} idea={idea} />
                ))}
              </div>

              {ideas.length > 3 && (
                <Button 
                  variant="ghost" 
                  onClick={() => setExpanded(!expanded)}
                  className="text-blue-600 hover:text-blue-800 flex items-center gap-2"
                >
                  {expanded ? 'Show less' : 'See more ideas'}
                  <ChevronRight className={`transform transition-transform ${expanded ? 'rotate-90' : ''}`} />
                </Button>
              )}
            </div>
          </CardContent>
        </div>
        <div className="w-1/3 relative">
          <img 
            src={getImage(index)}
            alt={title}
            className="w-full h-full object-cover"
          />
        </div>
      </div>
    </Card>
  );
};

const AddOpportunityCard = () => {
  const [newOpportunity, setNewOpportunity] = useState({
    title: '',
    description: ''
  });

  const handleNewOpportunity = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('New opportunity:', newOpportunity);
    setNewOpportunity({ title: '', description: '' });
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Card className="w-full h-48 mb-6 flex items-center justify-center hover:shadow-lg transition-shadow duration-300 cursor-pointer bg-gray-50">
          <div className="text-center">
            <Plus className="w-12 h-12 mx-auto mb-2 text-gray-400" />
            <p className="text-lg font-medium text-gray-600">Add New Opportunity</p>
          </div>
        </Card>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Opportunity</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleNewOpportunity} className="space-y-4 mt-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Title</label>
            <Input
              value={newOpportunity.title}
              onChange={(e) => setNewOpportunity(prev => ({ ...prev, title: e.target.value }))}
              placeholder="Enter opportunity title"
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Description</label>
            <Textarea
              value={newOpportunity.description}
              onChange={(e) => setNewOpportunity(prev => ({ ...prev, description: e.target.value }))}
              placeholder="Enter opportunity description"
              rows={4}
            />
          </div>
          <div className="flex justify-end gap-2">
            <DialogTrigger asChild>
              <Button variant="outline">Cancel</Button>
            </DialogTrigger>
            <Button type="submit">Add Opportunity</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

const GenerateOpportunityCard = () => (
  <Card className="w-full h-48 mb-6 flex items-center justify-center hover:shadow-lg transition-shadow duration-300 cursor-pointer bg-blue-50">
    <div className="text-center">
      <Sparkles className="w-12 h-12 mx-auto mb-2 text-blue-400" />
      <p className="text-lg font-medium text-blue-600">Generate New Opportunities</p>
    </div>
  </Card>
);

const OpportunitiesView = () => {
  const opportunities = [
    {
      title: "Tech-Enhanced Taste: Personalized Gelato Experiences",
      description: "Leverage technology to personalize gelato offerings, enhance production efficiency, and create immersive customer experiences both in-store and online.",
      ideas: [
        {
          title: "AI Flavor Matchmaker App",
          content: "Develop an app that recommends gelato flavors based on individual taste profiles...",
          fullContent: "Develop an app that recommends gelato flavors based on individual taste profiles and dietary preferences. The app will use machine learning to analyze user preferences and create personalized flavor suggestions."
        },
        {
          title: "Interactive In-Store Tablets",
          content: "Install kiosks where customers can customize their gelato orders digitally...",
          fullContent: "Install kiosks where customers can customize their gelato orders digitally. These tablets will feature an intuitive interface for flavor exploration, nutritional information, and custom combination suggestions."
        },
        {
          title: "Virtual Gelato Workshops",
          content: "Host online classes teaching gelato-making techniques...",
          fullContent: "Host online classes teaching gelato-making techniques. These interactive sessions will cover traditional methods, modern innovations, and tips for creating perfect gelato at home."
        },
        {
          title: "AR Packaging Experience",
          content: "Use AR to allow customers to scan packaging and learn about ingredient origins...",
          fullContent: "Use AR to allow customers to scan packaging and learn about ingredient origins. This interactive experience will showcase the sourcing journey, nutritional facts, and suggest flavor pairings."
        },
        {
          title: "Smart Production Systems",
          content: "Implement AI-driven analytics to optimize recipes...",
          fullContent: "Implement AI-driven analytics to optimize recipes and production processes. This system will analyze customer preferences, seasonal trends, and inventory data to improve efficiency and reduce waste."
        }
      ]
    },
    {
      title: "Tradition Reinvented: Classic Flavors, Healthier Choices",
      description: "Reimagine traditional Italian gelato flavors using plant-based and low-sugar ingredients, preserving the authentic taste and texture that appeals to both traditionalists and health-conscious consumers.",
      ideas: [
        {
          title: "Nonna's Pistachio Reborn",
          content: "A plant-based, low-sugar version of classic pistachio gelato...",
          fullContent: "A plant-based, low-sugar version of classic pistachio gelato that maintains the rich, creamy texture using innovative natural ingredients and sweeteners."
        },
        {
          title: "Dairy-Free Stracciatella",
          content: "Recreate the beloved chocolate chip gelato using almond milk...",
          fullContent: "Recreate the beloved chocolate chip gelato using almond milk base, with specially formulated dairy-free chocolate that maintains the signature 'stracciatella' texture."
        },
        {
          title: "Heritage Hazelnut Delight",
          content: "A lactose-free hazelnut gelato...",
          fullContent: "A lactose-free hazelnut gelato that celebrates traditional Italian flavors while catering to modern dietary needs. Made with premium Italian hazelnuts and dairy alternatives."
        },
        {
          title: "Sugar-Conscious Tiramisu",
          content: "A low-sugar take on the classic Italian dessert...",
          fullContent: "A low-sugar take on the classic Italian dessert, using natural sweeteners and innovative coffee infusion techniques to maintain authentic flavor profiles."
        },
        {
          title: "Classic Lemon Zest Sorbetto",
          content: "An all-natural, plant-based lemon sorbet...",
          fullContent: "An all-natural, plant-based lemon sorbet made with organic citrus and natural sweeteners, capturing the essence of traditional Italian sorbetto."
        }
      ]
    },
    {
      title: "Functional Indulgence: Gelato That Nourishes",
      description: "Introduce gelato infused with functional ingredients like probiotics, antioxidants, and superfoods, offering health benefits beyond basic nutrition while delivering indulgent taste.",
      ideas: [
        {
          title: "Antioxidant Berry Boost Gelato",
          content: "A plant-based gelato made with acai berries and blueberries...",
          fullContent: "A plant-based gelato made with acai berries and blueberries, rich in antioxidants for a boost of flavor and health benefits."
        },
        {
          title: "Probiotic Passion Fruit Gelato",
          content: "Incorporate gut-friendly probiotics into tropical flavors...",
          fullContent: "Incorporate gut-friendly probiotics into tropical flavors for a delicious and healthy treat. The probiotics contribute to digestive well-being."
        },
        {
          title: "Matcha Green Tea Fusion",
          content: "A gelato blending matcha with almond milk...",
          fullContent: "A gelato blending matcha with almond milk for a subtly sweet and earthy flavor, packed with antioxidants."
        },
        {
          title: "Turmeric Ginger Glow",
          content: "An anti-inflammatory gelato with coconut milk...",
          fullContent: "An anti-inflammatory gelato with coconut milk, combining the warming spices of turmeric and ginger for a unique flavor experience."
        },
        {
          title: "Chia Seed and Mango Medley",
          content: "A refreshing gelato with omega-3-rich chia seeds...",
          fullContent: "A refreshing gelato with omega-3-rich chia seeds and sweet mango for a healthy and flavorful delight."
        }
      ]
    },
    {
      title: "Sustainable Scoop: Ethical Gelato Without the Premium Price",
      description: "Adopt sustainable production and packaging practices to produce eco-friendly gelato options that do not significantly increase costs for consumers.",
      ideas: [
        {
          title: "Eco-Packaging Initiative",
          content: "Transition to biodegradable cups and spoons...",
          fullContent: "Transition to biodegradable cups and spoons, reducing environmental impact without compromising on quality or convenience."
        },
        {
          title: "Local Farm Partnerships",
          content: "Source ingredients from nearby farms...",
          fullContent: "Source ingredients from nearby farms, supporting local communities and reducing transportation emissions."
        },
        {
          title: "Solar-Powered Production",
          content: "Invest in renewable energy for facilities...",
          fullContent: "Invest in renewable energy for facilities, reducing carbon footprint and promoting sustainable practices."
        },
        {
          title: "Upcycled Ingredient Line",
          content: "Create flavors using upcycled fruits and nuts...",
          fullContent: "Create flavors using upcycled fruits and nuts, minimizing waste and promoting resource efficiency."
        },
        {
          title: "Transparency Labels",
          content: "Detail the sustainable journey of each product...",
          fullContent: "Detail the sustainable journey of each product, increasing consumer awareness and promoting responsible consumption."
        }
      ]
    }
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">Opportunity Spaces</h1>
      <div className="grid grid-cols-1 gap-6">
        {opportunities.map((opp, index) => (
          <OpportunityCard key={index} {...opp} index={index} />
        ))}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AddOpportunityCard />
          <GenerateOpportunityCard />
        </div>
      </div>
    </div>
  );
};

export default OpportunitiesView;