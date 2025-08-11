/**
 * Message utilities for formatting and parsing chat messages
 */

export interface FormattedMessage {
  content: string;
  type: 'text' | 'code' | 'list' | 'table' | 'link';
  metadata?: Record<string, any>;
}

/**
 * Format a message for display
 */
export function formatMessage(content: string): FormattedMessage[] {
  const formatted: FormattedMessage[] = [];
  
  // Split content by code blocks
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  let lastIndex = 0;
  let match;
  
  while ((match = codeBlockRegex.exec(content)) !== null) {
    // Add text before code block
    if (match.index > lastIndex) {
      const textContent = content.slice(lastIndex, match.index);
      if (textContent.trim()) {
        formatted.push({
          content: textContent.trim(),
          type: 'text'
        });
      }
    }
    
    // Add code block
    formatted.push({
      content: match[2],
      type: 'code',
      metadata: { language: match[1] || 'text' }
    });
    
    lastIndex = match.index + match[0].length;
  }
  
  // Add remaining text
  if (lastIndex < content.length) {
    const remainingText = content.slice(lastIndex);
    if (remainingText.trim()) {
      formatted.push({
        content: remainingText.trim(),
        type: 'text'
      });
    }
  }
  
  // If no code blocks found, return as single text message
  if (formatted.length === 0) {
    formatted.push({
      content: content.trim(),
      type: 'text'
    });
  }
  
  return formatted;
}

/**
 * Parse a message to extract structured data
 */
export function parseMessage(content: string): {
  text: string;
  codeBlocks: Array<{ language: string; code: string }>;
  links: string[];
  lists: string[][];
} {
  const result = {
    text: content,
    codeBlocks: [] as Array<{ language: string; code: string }>,
    links: [] as string[],
    lists: [] as string[][]
  };
  
  // Extract code blocks
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  let match;
  while ((match = codeBlockRegex.exec(content)) !== null) {
    result.codeBlocks.push({
      language: match[1] || 'text',
      code: match[2]
    });
  }
  
  // Extract links
  const linkRegex = /https?:\/\/[^\s]+/g;
  result.links = content.match(linkRegex) || [];
  
  // Extract lists
  const lines = content.split('\n');
  const currentList: string[] = [];
  
  for (const line of lines) {
    if (line.match(/^[\s]*[-*+]\s+/)) {
      currentList.push(line.replace(/^[\s]*[-*+]\s+/, ''));
    } else if (line.match(/^[\s]*\d+\.\s+/)) {
      currentList.push(line.replace(/^[\s]*\d+\.\s+/, ''));
    } else if (currentList.length > 0) {
      result.lists.push([...currentList]);
      currentList.length = 0;
    }
  }
  
  if (currentList.length > 0) {
    result.lists.push(currentList);
  }
  
  return result;
}

/**
 * Truncate a message to a specified length
 */
export function truncateMessage(content: string, maxLength: number = 100): string {
  if (content.length <= maxLength) {
    return content;
  }
  
  return content.slice(0, maxLength) + '...';
}

/**
 * Extract key information from a message
 */
export function extractMessageInfo(content: string): {
  hasCode: boolean;
  hasLinks: boolean;
  hasLists: boolean;
  wordCount: number;
  estimatedReadTime: number;
} {
  const parsed = parseMessage(content);
  
  return {
    hasCode: parsed.codeBlocks.length > 0,
    hasLinks: parsed.links.length > 0,
    hasLists: parsed.lists.length > 0,
    wordCount: content.split(/\s+/).length,
    estimatedReadTime: Math.ceil(content.split(/\s+/).length / 200) // ~200 words per minute
  };
}

/**
 * Sanitize message content for safe display
 */
export function sanitizeMessage(content: string): string {
  return content
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+\s*=/gi, '');
}

/**
 * Format timestamp for display
 */
export function formatTimestamp(timestamp: Date): string {
  const now = new Date();
  const diff = now.getTime() - timestamp.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  
  if (minutes < 1) {
    return 'Just now';
  } else if (minutes < 60) {
    return `${minutes}m ago`;
  } else if (hours < 24) {
    return `${hours}h ago`;
  } else if (days < 7) {
    return `${days}d ago`;
  } else {
    return timestamp.toLocaleDateString();
  }
}

/**
 * Generate a message preview
 */
export function generateMessagePreview(content: string, maxLength: number = 50): string {
  const text = content.replace(/```[\s\S]*?```/g, '[code]');
  return truncateMessage(text, maxLength);
} 