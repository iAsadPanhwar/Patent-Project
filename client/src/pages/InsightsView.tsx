import React, { useState } from 'react';
import { ChevronDown, Plus, Square, CheckSquare, ChevronLeft, ChevronRight } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

interface InsightsViewProps {
  setCurrentPage: (page: string) => void;
}

const InsightsView: React.FC<InsightsViewProps> = ({ setCurrentPage }) => {
  const [selectedCards, setSelectedCards] = useState({
    keyInsights: new Set([0, 1, 2, 3, 4]),
    news: new Set(Array.from({ length: 10 }, (_, i) => i)),
    trends: new Set(Array.from({ length: 10 }, (_, i) => i)),
    customers: new Set(Array.from({ length: 10 }, (_, i) => i)),
    competitors: new Set(Array.from({ length: 10 }, (_, i) => i))
  });

  const [expandedSections, setExpandedSections] = useState({
    keyInsights: false,
    news: false,
    trends: false,
    customers: false,
    competitors: false
  });

  const [newInsight, setNewInsight] = useState({
    title: '',
    content: ''
  });

  const scrollKeyInsights = (direction: 'left' | 'right') => {
    const container = document.getElementById('key-insights-container');
    if (container) {
      const scrollAmount = 400; 
      container.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  const toggleCardSelection = (section: string, index: number) => {
    setSelectedCards(prev => {
      const newSet = new Set(prev[section]);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return { ...prev, [section]: newSet };
    });
  };

  const toggleSelectAll = (section: string, totalItems: number) => {
    setSelectedCards(prev => {
      const currentSet = prev[section];
      const newSet = new Set();
      if (currentSet.size < totalItems) {
        for (let i = 0; i < totalItems; i++) {
          newSet.add(i);
        }
      }
      return { ...prev, [section]: newSet };
    });
  };

  const toggleSectionExpand = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const keyInsights = Array(5).fill(null).map((_, index) => ({
    category: "Market Overview",
    title: `Key Insight ${index + 1}`,
    content: "Despite Germany being Europe's largest coffee consumer, there's a surprising surge in demand for herbal coffee alternatives. Health-conscious millennials are seeking the familiar coffee experience without caffeine's side effects.",
    sources: "Allied Market Research, Statista",
    impact: "Strong market potential for herbal coffee alternatives that maintain traditional coffee rituals."
  }));

  const generateItems = (prefix: string) => Array(10).fill(null).map((_, index) => ({
    title: `${prefix} ${index + 1}`,
    content: `Sample content for ${prefix.toLowerCase()} item ${index + 1}. This provides valuable insights for the project.`,
    sources: "Market Research, Industry Reports",
    relevance: `Important implications for project development and strategy.`
  }));

  const categoryInsights = {
    news: generateItems("News Item"),
    trends: generateItems("Market Trend"),
    customers: generateItems("Customer Segment"),
    competitors: generateItems("Competitor Analysis")
  };

  const InsightSection = ({ title, insights, section }: { title: string, insights: any[], section: string }) => (
    <div className="mb-8">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold capitalize">{title}</h3>
        <button 
          onClick={() => toggleSelectAll(section, insights.length)}
          className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg"
        >
          {selectedCards[section].size === insights.length ? 'Deselect All' : 'Select All'}
        </button>
      </div>
      <div className="overflow-x-auto">
        <div className="flex flex-wrap gap-4 mb-4">
          {insights.slice(0, expandedSections[section] ? undefined : 3).map((insight, index) => (
            <div key={index} className="bg-white p-4 rounded-lg shadow-sm w-[300px] relative">
              <button
                onClick={() => toggleCardSelection(section, index)}
                className="absolute top-4 right-4"
              >
                {selectedCards[section].has(index) ? 
                  <CheckSquare className="w-5 h-5 text-blue-600" /> : 
                  <Square className="w-5 h-5 text-gray-400" />
                }
              </button>
              <h4 className="font-bold mb-2 pr-8">{insight.title}</h4>
              <p className="text-sm text-gray-600 mb-3">{insight.content}</p>
              <p className="text-xs text-gray-500 mb-2">Sources: {insight.sources}</p>
              <p className="text-xs font-medium">Relevance: {insight.relevance}</p>
            </div>
          ))}
        </div>
        <button 
          onClick={() => toggleSectionExpand(section)}
          className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1 mx-auto"
        >
          {expandedSections[section] ? 'Show Less' : 'View More'}
          <ChevronDown className={`transform transition-transform ${expandedSections[section] ? 'rotate-180' : ''}`} />
        </button>
      </div>
    </div>
  );

  const handleNewInsight = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('New insight:', newInsight);
    setNewInsight({ title: '', content: '' }); 
  };

  const NewInsightDialog = () => (
    <Dialog>
      <DialogTrigger asChild>
        <div className="bg-white p-6 rounded-lg shadow-md w-[400px] shrink-0 border-2 border-dashed border-gray-300 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 transition-colors">
          <Plus className="w-8 h-8 text-gray-400 mb-2" />
          <p className="text-gray-600 font-medium">Add New Key Insight</p>
        </div>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Insight</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleNewInsight} className="space-y-4 mt-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Title</label>
            <Input
              value={newInsight.title}
              onChange={(e) => setNewInsight(prev => ({ ...prev, title: e.target.value }))}
              placeholder="Enter insight title"
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Content</label>
            <Textarea
              value={newInsight.content}
              onChange={(e) => setNewInsight(prev => ({ ...prev, content: e.target.value }))}
              placeholder="Enter insight content"
              rows={4}
            />
          </div>
          <div className="flex justify-end gap-2">
            <DialogTrigger asChild>
              <Button variant="outline">Cancel</Button>
            </DialogTrigger>
            <Button type="submit">Add Insight</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );

  const navigateToOpportunities = () => {
    setCurrentPage('opportunities');
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Insights</h1>

      <div className="bg-gray-50 p-4 rounded-lg mb-8">
        <p className="text-sm text-gray-600 mb-2">
          <span className="font-medium">Challenge:</span> Development of a Flagship Herbal Coffee Alternative for the German Market
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <span className="font-medium">Description:</span> Create a unique product specifically for health-conscious millennials in Germany that combines local flavor inspiration with health benefits
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-medium">Constraints:</span> Target retail price €14 per pack, adapting to target segment consumer tastes, ensuring limited overlap with existing products
        </p>
      </div>

      <div className="mb-12">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Key Insights</h2>
          <div className="flex gap-2">
            <button 
              onClick={() => toggleSelectAll('keyInsights', keyInsights.length)}
              className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg"
            >
              {selectedCards.keyInsights.size === keyInsights.length ? 'Deselect All' : 'Select All'}
            </button>
            <button 
              onClick={navigateToOpportunities}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Generate Opportunities
            </button>
          </div>
        </div>
        <div className="relative group">
          <div className="overflow-x-auto" id="key-insights-container">
            <div className="flex space-x-6 pb-4 min-w-full">
              {keyInsights.map((insight, index) => (
                <div key={index} className="bg-white p-6 rounded-lg shadow-md w-[400px] shrink-0 relative">
                  <button
                    onClick={() => toggleCardSelection('keyInsights', index)}
                    className="absolute top-4 right-4"
                  >
                    {selectedCards.keyInsights.has(index) ? 
                      <CheckSquare className="w-5 h-5 text-blue-600" /> : 
                      <Square className="w-5 h-5 text-gray-400" />
                    }
                  </button>
                  <div className="text-sm text-blue-600 mb-2">{insight.category}</div>
                  <h3 className="font-bold mb-3 pr-8">{insight.title}</h3>
                  <p className="text-gray-600 mb-4">{insight.content}</p>
                  <p className="text-sm text-gray-500 mb-2">Sources: {insight.sources}</p>
                  <p className="text-sm font-medium">Impact: {insight.impact}</p>
                </div>
              ))}
              <NewInsightDialog />
            </div>
          </div>
          <button 
            onClick={() => scrollKeyInsights('left')} 
            className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <ChevronLeft className="w-6 h-6 text-gray-600" />
          </button>
          <button 
            onClick={() => scrollKeyInsights('right')} 
            className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white rounded-full p-2 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <ChevronRight className="w-6 h-6 text-gray-600" />
          </button>
        </div>
      </div>

      <InsightSection title="News" insights={categoryInsights.news} section="news" />
      <InsightSection title="Trends" insights={categoryInsights.trends} section="trends" />
      <InsightSection title="Customers" insights={categoryInsights.customers} section="customers" />
      <InsightSection title="Competitors" insights={categoryInsights.competitors} section="competitors" />

      <div className="space-y-8 mt-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold mb-4">Patents Research</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">Patent ID</th>
                  <th className="text-left py-3 px-4">Title</th>
                  <th className="text-left py-3 px-4">Assignee</th>
                  <th className="text-left py-3 px-4">Relevance</th>
                </tr>
              </thead>
              <tbody>
                {Array(5).fill(null).map((_, index) => (
                  <tr key={index} className="border-b">
                    <td className="py-3 px-4">PAT{String(index + 1).padStart(6, '0')}</td>
                    <td className="py-3 px-4">Eco-friendly Material Processing Method</td>
                    <td className="py-3 px-4">Sustainable Materials Corp</td>
                    <td className="py-3 px-4">High</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold mb-4">Academic Research</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4">Paper Title</th>
                  <th className="text-left py-3 px-4">Authors</th>
                  <th className="text-left py-3 px-4">Journal</th>
                  <th className="text-left py-3 px-4">Year</th>
                  <th className="text-left py-3 px-4">Key Findings</th>
                </tr>
              </thead>
              <tbody>
                {Array(5).fill(null).map((_, index) => (
                  <tr key={index} className="border-b">
                    <td className="py-3 px-4">Sustainable Materials in Eyewear</td>
                    <td className="py-3 px-4">Smith et al.</td>
                    <td className="py-3 px-4">Journal of Sustainable Materials</td>
                    <td className="py-3 px-4">2024</td>
                    <td className="py-3 px-4">Novel bio-based polymer with high durability</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="flex justify-center mt-8 mb-4">
        <button 
          onClick={navigateToOpportunities}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Generate Opportunities
        </button>
      </div>
    </div>
  );
};

export default InsightsView;