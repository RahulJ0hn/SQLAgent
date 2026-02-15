import { Table } from "lucide-react";

export default function ResultTable({ columns, data, rowCount }) {
  if (!data.length) {
    return (
      <div className="text-gray-400 text-sm p-4 text-center">
        No results returned
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-700 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <Table className="w-4 h-4" />
          Results
        </div>
        <span className="text-xs text-gray-500">{rowCount} rows</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-800/50">
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-4 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider whitespace-nowrap"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {data.slice(0, 50).map((row, i) => (
              <tr key={i} className="hover:bg-gray-800/30 transition-colors">
                {columns.map((col) => (
                  <td
                    key={col}
                    className="px-4 py-2 text-gray-300 whitespace-nowrap"
                  >
                    {String(row[col] ?? "")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {rowCount > 50 && (
        <div className="px-4 py-2 bg-gray-800/50 text-xs text-gray-500 text-center border-t border-gray-700">
          Showing 50 of {rowCount} rows
        </div>
      )}
    </div>
  );
}
