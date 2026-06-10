import { useState, useRef, useEffect } from 'react';
import { Car, ToolCallRecord, chatAPI } from '../services/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCallRecord[];
  toolContent?: string; // Raw tool output for detection
}

interface ChatAssistantProps {
  currentCar?: Car;
  currentCars: Car[];
  savedCars: Car[];
}

interface VehicleDetails {
  title: string;
  [key: string]: string;
}

interface WebSearchResult {
  title: string;
  url?: string;
  snippet?: string;
}

interface ComparisonData {
  raw: string;
}

const SUGGESTED_QUESTIONS = [
  'What cars are on this page?',
  'Which saved car is cheapest?',
  'Compare the first two cars',
  'Is this a good option for the mileage and price?',
];

function formatToolArgs(args: Record<string, unknown>): string {
  if (!Object.keys(args).length) return '()';
  const parts = Object.entries(args).map(([k, v]) => {
    if (Array.isArray(v)) return `${k}: [${(v as unknown[]).join(', ')}]`;
    return `${k}: ${JSON.stringify(v)}`;
  });
  return `(${parts.join(', ')})`;
}

function ToolActivity({ toolCalls }: { toolCalls: ToolCallRecord[] }) {
  return (
    <div style={{
      marginBottom: '0.5rem',
      paddingLeft: '0.6rem',
      borderLeft: '3px solid #e67e22',
    }}>
      {toolCalls.map((tc, i) => (
        <div key={i} style={{
          fontSize: '0.72rem',
          color: '#888',
          marginBottom: '0.2rem',
          fontFamily: 'monospace',
          display: 'flex',
          flexWrap: 'wrap',
          gap: '0.25rem',
          alignItems: 'center',
        }}>
          <span style={{ color: '#e67e22' }}>⚙</span>
          <span style={{ color: '#c0392b', fontWeight: 600 }}>{tc.tool}</span>
          <span style={{ color: '#aaa' }}>{formatToolArgs(tc.args)}</span>
          <span style={{ color: '#bbb' }}>→</span>
          <span style={{ color: '#666' }}>{tc.result_summary}</span>
        </div>
      ))}
    </div>
  );
}

// Parser for get_vehicle_details response
function parseVehicleDetails(text: string): VehicleDetails | null {
  const lines = text.split('\n').filter(l => l.trim());
  if (lines.length < 3) return null;
  
  const details: VehicleDetails = { title: '' };
  const titleLine = lines[0];
  if (titleLine && !titleLine.includes('not found')) {
    details.title = titleLine;
    for (const line of lines.slice(1)) {
      const match = line.match(/^([^:]+):\s+(.*)$/);
      if (match) {
        details[match[1].toLowerCase().trim()] = match[2].trim();
      }
    }
    return Object.keys(details).length > 1 ? details : null;
  }
  return null;
}

// Pretty render for vehicle details
function VehicleDetailsCard({ details }: { details: VehicleDetails }) {
  const price = details.price ? details.price.replace('$', '') : 'N/A';
  const mileageNum = parseInt(details.mileage || '0');
  const priceNum = parseInt(price.replace(/,/g, '') || '0');
  const ratio = mileageNum > 0 ? (priceNum / mileageNum).toFixed(2) : 'N/A';

  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      borderRadius: '8px',
      padding: '1rem',
      color: 'white',
      marginBottom: '0.5rem',
    }}>
      <div style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.6rem' }}>
        {details.title}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem', fontSize: '0.9rem' }}>
        <div>
          <div style={{ opacity: 0.8, fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.2rem' }}>Price</div>
          <div style={{ fontSize: '1.3rem', fontWeight: 'bold' }}>{details.price}</div>
        </div>
        <div>
          <div style={{ opacity: 0.8, fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.2rem' }}>Mileage</div>
          <div style={{ fontSize: '1.1rem' }}>{details.mileage}</div>
        </div>
        <div>
          <div style={{ opacity: 0.8, fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.2rem' }}>Location</div>
          <div>{details.location || 'N/A'}</div>
        </div>
        <div>
          <div style={{ opacity: 0.8, fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: '0.2rem' }}>$/Mile</div>
          <div>${ratio}</div>
        </div>
      </div>
      {details.vin && (
        <div style={{ marginTop: '0.6rem', paddingTop: '0.6rem', borderTop: '1px solid rgba(255,255,255,0.2)', fontSize: '0.8rem', opacity: 0.9 }}>
          <strong>VIN:</strong> {details.vin}
        </div>
      )}
      {details.notes && (
        <div style={{ marginTop: '0.4rem', fontSize: '0.8rem', opacity: 0.9 }}>
          <strong>Notes:</strong> {details.notes}
        </div>
      )}
    </div>
  );
}

// Parser for web_search response
function parseWebSearchResults(text: string): WebSearchResult[] | null {
  if (!text.includes('Web results for')) return null;
  
  const results: WebSearchResult[] = [];
  // const sections = text.split('\n\n');
  let currentResult: WebSearchResult = { title: '' };

  for (const line of text.split('\n')) {
    if (line.startsWith('• ')) {
      if (Object.keys(currentResult).length > 0) results.push(currentResult);
      currentResult = { title: line.substring(2) };
    } else if (line.startsWith('  ') && currentResult.title) {
      const content = line.trim();
      if (content.startsWith('http')) {
        currentResult.url = content;
      } else {
        currentResult.snippet = content;
      }
    }
  }
  if (Object.keys(currentResult).length > 0) results.push(currentResult);
  
  return results.length > 0 ? results : null;
}

// Pretty render for web search results
function WebSearchResults({ results }: { results: WebSearchResult[] }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginBottom: '0.5rem' }}>
      {results.map((r, i) => (
        <div
          key={i}
          style={{
            background: '#f8f9fa',
            border: '1px solid #e0e0e0',
            borderRadius: '6px',
            padding: '0.7rem',
            cursor: r.url ? 'pointer' : 'default',
            transition: 'all 0.2s',
            hover: r.url ? { background: '#eaf4fb', borderColor: '#3498db' } : {},
          }}
          onClick={() => r.url && window.open(r.url, '_blank')}
          onMouseOver={e => {
            if (r.url) {
              (e.currentTarget as HTMLElement).style.background = '#eaf4fb';
              (e.currentTarget as HTMLElement).style.borderColor = '#3498db';
            }
          }}
          onMouseOut={e => {
            (e.currentTarget as HTMLElement).style.background = '#f8f9fa';
            (e.currentTarget as HTMLElement).style.borderColor = '#e0e0e0';
          }}
        >
          <div style={{ fontWeight: 600, color: '#0066cc', fontSize: '0.9rem', marginBottom: '0.3rem' }}>
            {r.title}
          </div>
          {r.snippet && (
            <div style={{ fontSize: '0.8rem', color: '#666', marginBottom: '0.3rem', lineHeight: '1.4' }}>
              {r.snippet}
            </div>
          )}
          {r.url && (
            <div style={{ fontSize: '0.7rem', color: '#999', fontFamily: 'monospace' }}>
              🔗 {r.url.substring(0, 60)}...
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

// Parser for compare_cars response
function parseComparison(text: string): ComparisonData | null {
  if (!text.includes('Cheapest:') && !text.includes('Best')) return null;
  return { raw: text };
}

// Pretty render for comparison
function ComparisonCard({ data }: { data: ComparisonData }) {
  return (
    <div style={{
      background: '#f9fafb',
      border: '1px solid #e5e7eb',
      borderRadius: '6px',
      padding: '0.8rem',
      fontFamily: 'monospace',
      fontSize: '0.75rem',
      lineHeight: '1.6',
      overflowX: 'auto',
    }}>
      {data.raw.split('\n').map((line: string, i: number) => (
        <div key={i} style={{
          color: line.includes('Cheapest') || line.includes('Best') || line.includes('Lowest') ? '#d97706' : '#666',
          fontWeight: line.includes('Cheapest') || line.includes('Best') || line.includes('Lowest') ? 600 : 400,
        }}>
          {line}
        </div>
      ))}
    </div>
  );
}

export function ChatAssistant({ currentCar, currentCars, savedCars }: ChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hi! I'm your CarScope AI agent. I can look up cars on this page, compare listings, check your saved cars, and search the web for reviews and reliability info.",
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const send = async (text: string) => {
    if (!text.trim() || loading) return;

    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await chatAPI.ask({
        question: text,
        current_car_id: currentCar?.id,
        saved_car_ids: savedCars.map(c => c.id),
        current_cars_snapshot: currentCars,
        saved_cars_snapshot: savedCars,
      });

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: response.data.answer,
          toolCalls: response.data.tool_calls,
        },
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, something went wrong. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">🤖 AI Agent</div>

      <div className="chat-messages">
        {messages.map((msg, idx) => {
          // Detect tool type from tool calls
          const toolType = msg.toolCalls?.[0]?.tool;
          
          // Try to parse and render tool-specific responses
          let vehicleDetails = null;
          let webResults = null;
          let comparison = null;
          
          if (toolType === 'get_vehicle_details' && msg.content) {
            vehicleDetails = parseVehicleDetails(msg.content);
          } else if (toolType === 'web_search' && msg.content) {
            webResults = parseWebSearchResults(msg.content);
          } else if (toolType === 'compare_cars' && msg.content) {
            comparison = parseComparison(msg.content);
          }

          return (
            <div key={idx} className={`chat-message ${msg.role}`}>
              {msg.role === 'assistant' && msg.toolCalls && msg.toolCalls.length > 0 && (
                <ToolActivity toolCalls={msg.toolCalls} />
              )}
              
              {vehicleDetails && (
                <VehicleDetailsCard details={vehicleDetails} />
              )}
              
              {webResults && (
                <WebSearchResults results={webResults} />
              )}
              
              {comparison && (
                <ComparisonCard data={comparison} />
              )}
              
              {!vehicleDetails && !webResults && !comparison && (
                <div
                  className={`message-content ${msg.role}`}
                  style={{ whiteSpace: 'pre-wrap' }}
                >
                  {msg.content}
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div className="chat-message assistant">
            <div style={{
              paddingLeft: '0.6rem',
              borderLeft: '3px solid #e67e22',
              marginBottom: '0.4rem',
              fontSize: '0.72rem',
              color: '#e67e22',
              fontFamily: 'monospace',
            }}>
              ⚙ Agent working...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Suggested questions — shown only on initial state */}
      {messages.length <= 1 && (
        <div style={{ marginBottom: '0.75rem' }}>
          <div style={{ fontSize: '0.73rem', color: '#aaa', marginBottom: '0.4rem', fontWeight: 500 }}>
            Try asking:
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.3rem' }}>
            {SUGGESTED_QUESTIONS.map(q => (
              <button
                key={q}
                onClick={() => send(q)}
                style={{
                  background: '#f8f9fa',
                  border: '1px solid #e8e8e8',
                  borderRadius: '4px',
                  padding: '0.35rem 0.6rem',
                  fontSize: '0.78rem',
                  cursor: 'pointer',
                  textAlign: 'left',
                  color: '#555',
                  transition: 'background 0.15s, border-color 0.15s',
                }}
                onMouseOver={e => {
                  e.currentTarget.style.background = '#eaf4fb';
                  e.currentTarget.style.borderColor = '#3498db';
                }}
                onMouseOut={e => {
                  e.currentTarget.style.background = '#f8f9fa';
                  e.currentTarget.style.borderColor = '#e8e8e8';
                }}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="chat-input-group">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              send(inputValue);
            }
          }}
          disabled={loading}
        />
        <button
          className="button button-small"
          onClick={() => send(inputValue)}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}
