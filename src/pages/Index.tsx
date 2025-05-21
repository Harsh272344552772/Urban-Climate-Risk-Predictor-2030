
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';

interface ClimateData {
  temperature: { year: number; value: number }[];
  rainfall: { year: number; value: number }[];
}

export default function Index() {
  const [climateData, setClimateData] = useState<ClimateData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Add cache-busting parameter to prevent caching issues
        const response = await fetch(`/api/climate-data?t=${Date.now()}`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setClimateData(data);
        setLoading(false);
        setError(null);
      } catch (error) {
        console.error('Error fetching climate data:', error);
        setError('Failed to load climate data. Using demo data instead.');
        
        // Show toast with error message
        toast({
          title: "Data Loading Error",
          description: "Using fallback demo data. Please check your connection.",
          variant: "destructive",
        });
        
        // Use mock data if Flask backend is not available
        setClimateData({
          temperature: [
            { year: 2023, value: 25.8 },
            { year: 2024, value: 26.2 },
            { year: 2025, value: 26.7 },
            { year: 2030, value: 29.0 }
          ],
          rainfall: [
            { year: 2023, value: 800 },
            { year: 2024, value: 750 },
            { year: 2025, value: 900 },
            { year: 2030, value: 600 }
          ]
        });
        setLoading(false);
      }
    };

    fetchData();
  }, [toast]);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-primary text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Urban Climate Risk Predictor</h1>
          <nav>
            <ul className="flex gap-4">
              <li><Link to="/" className="text-white hover:underline">Home</Link></li>
              <li><Link to="/contact" className="text-white hover:underline">Contact</Link></li>
              <li><Link to="/login" className="text-white hover:underline">Login</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="flex-1 container mx-auto p-4">
        <section className="py-12 text-center">
          <h2 className="text-3xl font-bold mb-4">Urban Climate Risk Predictor 2030</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Forecast climate risks for urban areas and get actionable recommendations to build resilience.
          </p>
          <div className="flex justify-center gap-4">
            <Button asChild size="lg">
              <Link to="/predict">Try Risk Prediction</Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link to="/about">Learn More</Link>
            </Button>
          </div>
        </section>

        {error && (
          <div className="bg-destructive/10 text-destructive p-4 rounded-md mb-8">
            {error}
          </div>
        )}

        <section className="py-8">
          <h3 className="text-2xl font-bold mb-6 text-center">Climate Visualizations</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Temperature Projections</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <p>Loading temperature data...</p>
                ) : climateData ? (
                  <ul className="space-y-2">
                    {climateData.temperature.map((item) => (
                      <li key={item.year} className="flex justify-between">
                        <span>Year {item.year}:</span>
                        <span className="font-medium">{item.value}°C</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No temperature data available</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Rainfall Projections</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <p>Loading rainfall data...</p>
                ) : climateData ? (
                  <ul className="space-y-2">
                    {climateData.rainfall.map((item) => (
                      <li key={item.year} className="flex justify-between">
                        <span>Year {item.year}:</span>
                        <span className="font-medium">{item.value} mm</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No rainfall data available</p>
                )}
              </CardContent>
            </Card>
          </div>
        </section>
      </main>

      <footer className="bg-muted p-6 text-center">
        <p>© {new Date().getFullYear()} Urban Climate Risk Predictor. All rights reserved.</p>
      </footer>
    </div>
  );
}
