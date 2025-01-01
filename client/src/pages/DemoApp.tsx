import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Menu, X, Home, FileText, Lightbulb, Settings, Upload, ChevronDown, Target } from 'lucide-react';
import InsightsView from './InsightsView';
import OpportunitiesView from './OpportunitiesView';
import CompanyEditForm from './CompanyEditForm';

const DemoApp = () => {
  const [currentPage, setCurrentPage] = useState('login');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [selectedSources, setSelectedSources] = useState([]);

  const defaultProjectInfo = {
    name: "Eco-Friendly Materials Development for FLiPO Eyewear",
    description: "Develop eco-friendly materials for frames and lenses to meet growing consumer demand for sustainable products",
    purpose: "To align FLiPO Eyewear's product offerings with environmental sustainability trends, thereby attracting eco-conscious consumers and differentiating the brand in the competitive eyewear market",
    constraints: "Ensure materials meet durability standards while maintaining affordability; maintain aesthetic appeal and comfort; comply with industry regulations and standards"
  };

  const [currentProject, setCurrentProject] = useState(defaultProjectInfo);

  const projects = [
    {
      name: "Eco-Materials Research",
      description: "Analysis of sustainable materials for next-gen eyewear",
      status: "In Progress"
    },
    {
      name: "Market Analysis 2024",
      description: "Competitive landscape and consumer trends",
      status: "Completed"
    }
  ];

  const sourceOptions = [
    { id: 'patents', label: 'Patents' },
    { id: 'academic', label: 'Academic Research' },
    { id: 'trends', label: 'News Trends' },
    { id: 'customers', label: 'Customers' },
    { id: 'competitors', label: 'Competitors' }
  ];

  const Sidebar = () => {
    const [expandedProject, setExpandedProject] = useState<string | null>(null);

    return (
      <div className={`fixed inset-y-0 left-0 w-64 bg-white shadow-lg transform ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-200 ease-in-out z-30`}>
        <div className="p-4">
          <button onClick={() => setIsSidebarOpen(false)} className="mb-4">
            <X size={24} />
          </button>
          <nav className="space-y-6">
            <button 
              onClick={() => { setCurrentPage('dashboard'); setIsSidebarOpen(false); }}
              className="flex items-center space-x-2 w-full p-2 hover:bg-gray-100 rounded"
            >
              <Home size={20} />
              <span>Dashboard</span>
            </button>

            <div className="space-y-2">
              {projects.map((project) => (
                <div key={project.name} className="space-y-1">
                  <button
                    onClick={() => setExpandedProject(expandedProject === project.name ? null : project.name)}
                    className="flex items-center justify-between w-full p-2 hover:bg-gray-100 rounded text-sm"
                  >
                    <span className="truncate">{project.name}</span>
                    <ChevronDown
                      size={16}
                      className={`transform transition-transform ${
                        expandedProject === project.name ? 'rotate-180' : ''
                      }`}
                    />
                  </button>

                  {expandedProject === project.name && (
                    <div className="pl-4 space-y-1">
                      <button 
                        onClick={() => { setCurrentPage('insights'); setIsSidebarOpen(false); }}
                        className="flex items-center space-x-2 w-full p-2 hover:bg-gray-100 rounded text-sm"
                      >
                        <Lightbulb size={16} />
                        <span>Insights</span>
                      </button>
                      <button 
                        onClick={() => { setCurrentPage('opportunities'); setIsSidebarOpen(false); }}
                        className="flex items-center space-x-2 w-full p-2 hover:bg-gray-100 rounded text-sm"
                      >
                        <Target size={16} />
                        <span>Opportunities</span>
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </nav>
        </div>
      </div>
    );
  };

  const Header = () => (
    <div className="bg-white p-4 shadow-sm flex items-center">
      <button onClick={() => setIsSidebarOpen(true)} className="p-2 hover:bg-gray-100 rounded">
        <Menu size={24} />
      </button>
      <h1 className="ml-4 text-xl font-semibold flex items-center">
        <span className="italic">TheBox</span>
        <span className="text-gray-500 ml-2">by Quartz Labs</span>
      </h1>
    </div>
  );

  const Login = () => {
    return (
      <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6">Login</h2>
        <div className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full p-2 border rounded"
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full p-2 border rounded"
          />
          <button 
            onClick={() => setCurrentPage('dashboard')}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
          >
            Login
          </button>
        </div>
      </div>
    );
  };

  const Dashboard = () => (
    <div className="max-w-6xl mx-auto mt-10 p-6">
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-xl font-semibold">FLiPO Eyewear</h3>
            <p className="text-gray-600 mt-1">Sector: Sustainable Fashion & Eyewear</p>
          </div>
          <button 
            onClick={() => setCurrentPage('editCompany')}
            className="text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            Edit
            <ChevronRight size={16} />
          </button>
        </div>
      </div>

      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">Projects</h2>
          <button 
            onClick={() => setCurrentPage('newProject')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2"
          >
            <FileText size={20} />
            New Project
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {projects.map((project) => (
            <div key={project.name} className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold">{project.name}</h3>
              <p className="text-gray-600 mt-2">{project.description}</p>
              <div className="mt-4">
                <span className={`px-3 py-1 ${
                  project.status === 'In Progress' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                } rounded-full text-sm`}>
                  {project.status}
                </span>
              </div>
              <button 
                onClick={() => setCurrentPage('insights')}
                className="mt-4 text-blue-600 flex items-center gap-1"
              >
                View Insights
                <ChevronRight size={16} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const NewProject = () => {
    const [dragActive, setDragActive] = useState(false);
    const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
    const fileInputRef = React.useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      if (e.type === "dragenter" || e.type === "dragover") {
        setDragActive(true);
      } else if (e.type === "dragleave") {
        setDragActive(false);
      }
    };

    const handleDrop = (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);

      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFiles(Array.from(e.dataTransfer.files));
      }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      e.preventDefault();
      if (e.target.files && e.target.files[0]) {
        handleFiles(Array.from(e.target.files));
      }
    };

    const handleFiles = (files: File[]) => {
      setUploadedFiles(prev => [...prev, ...files]);
    };

    const onButtonClick = () => {
      fileInputRef.current?.click();
    };

    return (
      <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6">New Project</h2>
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-1">Project Name</label>
            <input
              defaultValue={defaultProjectInfo.name}
              className="w-full p-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Challenge Description</label>
            <textarea
              defaultValue={defaultProjectInfo.description}
              className="w-full p-2 border rounded"
              rows={3}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Purpose</label>
            <textarea
              defaultValue={defaultProjectInfo.purpose}
              className="w-full p-2 border rounded"
              rows={3}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Focus/Constraints</label>
            <textarea
              defaultValue={defaultProjectInfo.constraints}
              className="w-full p-2 border rounded"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Upload Source</label>
            <div 
              className={`mt-2 border-2 ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'} ${
                dragActive ? '' : 'border-dashed'
              } rounded-lg p-6 text-center relative`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                multiple
                onChange={handleChange}
              />
              <Upload className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2 text-sm text-gray-600">
                {dragActive ? (
                  "Drop files here..."
                ) : (
                  <>
                    Drag and drop files here, or{" "}
                    <button
                      onClick={onButtonClick}
                      className="text-blue-600 hover:text-blue-700"
                    >
                      browse
                    </button>
                  </>
                )}
              </p>
              {uploadedFiles.length > 0 && (
                <div className="mt-4 space-y-2">
                  <p className="text-sm font-medium">Uploaded files:</p>
                  {uploadedFiles.map((file, index) => (
                    <div key={index} className="text-sm text-gray-600 flex items-center gap-2">
                      <div className="w-4 h-4 rounded-full bg-green-500" />
                      {file.name}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="font-medium">Select Sources</h3>
            <div className="grid grid-cols-2 gap-4">
              {sourceOptions.map((source) => (
                <label key={source.id} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={selectedSources.includes(source.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedSources([...selectedSources, source.id]);
                      } else {
                        setSelectedSources(selectedSources.filter(id => id !== source.id));
                      }
                    }}
                    className="form-checkbox"
                  />
                  <span>{source.label}</span>
                </label>
              ))}
            </div>
          </div>

          <button 
            onClick={() => setCurrentPage('insights')}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
          >
            Generate Insights
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      {currentPage !== 'login' && <Sidebar />}
      <div className={`${currentPage !== 'login' ? 'pt-4' : ''}`}>
        {currentPage === 'login' && <Login />}
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'newProject' && <NewProject />}
        {currentPage === 'insights' && <InsightsView setCurrentPage={setCurrentPage} />}
        {currentPage === 'opportunities' && <OpportunitiesView />}
        {currentPage === 'editCompany' && <CompanyEditForm setCurrentPage={setCurrentPage} />}
      </div>
    </div>
  );
};

export default DemoApp;