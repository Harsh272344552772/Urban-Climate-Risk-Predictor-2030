
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/hooks/use-toast';

interface Prediction {
  id: number;
  city: string;
  population: number;
  temperature_increase: number;
  risk_level: string;
  risk_score: number;
  date: string;
}

interface Contact {
  id: number;
  name: string;
  email: string;
  message: string;
  date: string;
}

export default function Dashboard() {
  const { toast } = useToast();
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // In a real app, this would be a real API call
        // Simulating data fetch for now
        setTimeout(() => {
          setPredictions([
            {
              id: 1,
              city: "New York",
              population: 8500000,
              temperature_increase: 2.1,
              risk_level: "high",
              risk_score: 82,
              date: "2023-05-15"
            },
            {
              id: 2,
              city: "Los Angeles",
              population: 4000000,
              temperature_increase: 1.8,
              risk_level: "medium",
              risk_score: 65,
              date: "2023-05-14"
            },
            {
              id: 3,
              city: "Chicago",
              population: 2700000,
              temperature_increase: 1.5,
              risk_level: "low",
              risk_score: 35,
              date: "2023-05-12"
            }
          ]);

          setContacts([
            {
              id: 1,
              name: "Jane Smith",
              email: "jane@example.com",
              message: "I'm interested in using this tool for my research on urban planning.",
              date: "2023-05-16"
            },
            {
              id: 2,
              name: "Mark Johnson",
              email: "mark@example.com",
              message: "Can you provide more information about your methodology?",
              date: "2023-05-15"
            }
          ]);

          setLoading(false);
        }, 1000);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        toast({
          title: "Error",
          description: "Failed to load dashboard data",
          variant: "destructive",
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
              <li><Link to="/" className="text-white hover:underline">Logout</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="flex-1 container mx-auto p-4">
        <h2 className="text-3xl font-bold my-6">Dashboard</h2>

        <Tabs defaultValue="predictions">
          <TabsList className="mb-4">
            <TabsTrigger value="predictions">Predictions</TabsTrigger>
            <TabsTrigger value="contacts">Contact Messages</TabsTrigger>
          </TabsList>
          
          <TabsContent value="predictions">
            <Card>
              <CardHeader>
                <CardTitle>Your Recent Predictions</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <p>Loading predictions...</p>
                ) : predictions.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b">
                          <th className="text-left p-2">City</th>
                          <th className="text-left p-2">Population</th>
                          <th className="text-left p-2">Temp Increase</th>
                          <th className="text-left p-2">Risk Level</th>
                          <th className="text-left p-2">Risk Score</th>
                          <th className="text-left p-2">Date</th>
                        </tr>
                      </thead>
                      <tbody>
                        {predictions.map((prediction) => (
                          <tr key={prediction.id} className="border-b">
                            <td className="p-2">{prediction.city}</td>
                            <td className="p-2">{prediction.population.toLocaleString()}</td>
                            <td className="p-2">{prediction.temperature_increase}°C</td>
                            <td className="p-2 capitalize">{prediction.risk_level}</td>
                            <td className="p-2">{prediction.risk_score}%</td>
                            <td className="p-2">{prediction.date}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p>No predictions found. Try making some predictions first.</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="contacts">
            <Card>
              <CardHeader>
                <CardTitle>Contact Messages</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <p>Loading contacts...</p>
                ) : contacts.length > 0 ? (
                  <div className="space-y-4">
                    {contacts.map((contact) => (
                      <div key={contact.id} className="p-4 border rounded-lg">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-medium">{contact.name}</h3>
                            <p className="text-sm text-muted-foreground">{contact.email}</p>
                          </div>
                          <div className="text-sm text-muted-foreground">{contact.date}</div>
                        </div>
                        <p className="mt-2">{contact.message}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p>No contact messages found.</p>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      <footer className="bg-muted p-6 text-center">
        <p>© {new Date().getFullYear()} Urban Climate Risk Predictor. All rights reserved.</p>
      </footer>
    </div>
  );
}
