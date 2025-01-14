import { useState, useCallback } from 'react';
import { Toast, ToastProvider, ToastViewport } from '@/components/ui/toast';

type ToastType = 'default' | 'success' | 'destructive';

interface ToastMessage {
  id: string;
  type: ToastType;
  title: string;
  description?: string;
}

export const ToastContainer = ({ children }: { children: React.ReactNode }) => (
  <ToastProvider>
    {children}
    <ToastViewport />
  </ToastProvider>
);

export const useToast = () => {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = useCallback(
    (type: ToastType, title: string, description?: string) => {
      const id = Math.random().toString(36).substr(2, 9);
      setToasts((prev) => [...prev, { id, type, title, description }]);

      // Retirer automatiquement le toast après 5 secondes
      setTimeout(() => {
        setToasts((prev) => prev.filter((toast) => toast.id !== id));
      }, 5000);
    },
    []
  );

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const ToastList = useCallback(
    () => (
      <>
        {toasts.map((toast) => (
          <Toast key={toast.id} variant={toast.type} onOpenChange={() => removeToast(toast.id)}>
            <div>
              <div className="font-semibold">{toast.title}</div>
              {toast.description && (
                <div className="text-sm text-gray-500">{toast.description}</div>
              )}
            </div>
          </Toast>
        ))}
      </>
    ),
    [toasts, removeToast]
  );

  return {
    addToast,
    removeToast,
    ToastList,
  };
};
