
import { LucideIcon } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  stats: string;
}

export const FeatureCard = ({ icon: Icon, title, description, stats }: FeatureCardProps) => {
  return (
    <Card className="shadow-lg border-blue-100 hover:shadow-xl transition-all duration-300 hover:scale-105">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="p-3 bg-gradient-to-r from-blue-100 to-indigo-100 rounded-xl">
            <Icon className="h-6 w-6 text-blue-600" />
          </div>
          <Badge variant="secondary" className="bg-green-100 text-green-700">
            {stats}
          </Badge>
        </div>
        <CardTitle className="text-lg">{title}</CardTitle>
        <CardDescription className="text-sm leading-relaxed">
          {description}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full animate-pulse" style={{ width: '85%' }}></div>
        </div>
        <p className="text-xs text-gray-500 mt-2">System operational</p>
      </CardContent>
    </Card>
  );
};
