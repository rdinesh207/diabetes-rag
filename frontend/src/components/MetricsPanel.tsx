
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, Database, Zap, Clock } from 'lucide-react';

export const MetricsPanel = () => {
  const metrics = [
    {
      label: "Query Response Time",
      value: "1.2s",
      change: "-15%",
      icon: Clock,
      color: "text-green-600"
    },
    {
      label: "Vector Similarity",
      value: "94.3%",
      change: "+2.1%",
      icon: Database,
      color: "text-blue-600"
    },
    {
      label: "LLM Accuracy",
      value: "98.7%",
      change: "+0.8%",
      icon: Zap,
      color: "text-purple-600"
    },
    {
      label: "Papers Indexed",
      value: "10,247",
      change: "+156",
      icon: TrendingUp,
      color: "text-indigo-600"
    }
  ];

  return (
    <Card className="shadow-lg border-blue-100">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <TrendingUp className="h-5 w-5 text-green-600" />
          <span>System Metrics</span>
        </CardTitle>
        <CardDescription>Real-time performance indicators</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {metrics.map((metric, index) => (
          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-lg bg-white`}>
                <metric.icon className={`h-4 w-4 ${metric.color}`} />
              </div>
              <div>
                <p className="font-medium text-sm text-gray-900">{metric.label}</p>
                <p className="text-xs text-gray-600">Last 24h</p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-semibold text-lg">{metric.value}</p>
              <Badge 
                variant="secondary" 
                className={`text-xs ${
                  metric.change.startsWith('+') 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-blue-100 text-blue-700'
                }`}
              >
                {metric.change}
              </Badge>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
};
