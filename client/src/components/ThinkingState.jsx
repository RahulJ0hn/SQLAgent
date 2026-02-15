import { Brain, Database, Shield, RefreshCw } from "lucide-react";

const stepIcons = {
  Discovery: <Database className="w-4 h-4" />,
  Planner: <Brain className="w-4 h-4" />,
  Executor: <Database className="w-4 h-4" />,
  Guardrail: <Shield className="w-4 h-4" />,
  Validation: <Shield className="w-4 h-4" />,
};

function getIcon(step) {
  if (step.startsWith("Self-Heal")) return <RefreshCw className="w-4 h-4" />;
  return stepIcons[step] || <Brain className="w-4 h-4" />;
}

export default function ThinkingState({ steps, isLoading }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-sm text-gray-400 font-medium">
        <Brain className="w-4 h-4 text-blue-400" />
        Agent Reasoning
        {isLoading && (
          <span className="flex gap-1 ml-2">
            <span className="thinking-dot" />
            <span className="thinking-dot" />
            <span className="thinking-dot" />
          </span>
        )}
      </div>
      <div className="space-y-1">
        {steps.map((step, i) => (
          <div
            key={i}
            className="flex items-start gap-3 p-2 rounded-lg bg-gray-800/50 border border-gray-700/50 text-sm"
          >
            <div className="mt-0.5 text-blue-400 shrink-0">
              {getIcon(step.step)}
            </div>
            <div className="min-w-0">
              <span className="font-medium text-blue-300">{step.step}</span>
              <p className="text-gray-300 mt-0.5">{step.thought}</p>
              {step.action && (
                <p className="text-gray-500 text-xs mt-0.5 font-mono truncate">
                  {step.action}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
