import React, { useState, useRef, useEffect } from "react";
import { Button } from "../../components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/card";
import * as Dialog from "@radix-ui/react-dialog";
import * as Toast from "@radix-ui/react-toast";
import { FaStar } from "react-icons/fa";

interface Task {
  id: number;
  name: string;
  difficulty: number;
}

interface Leaderboard {
  id: number;
  name: string;
  users: { id: number; username: string; points: number }[];
}

interface User {
  email: string;
  password: string;
  username?: string;
}

export const LeaderboardFrame = (): JSX.Element => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [leaderboards, setLeaderboards] = useState<Leaderboard[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [selectedLeaderboard, setSelectedLeaderboard] = useState<Leaderboard | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
  const [user, setUser] = useState<User | null>(null);
  const [showNewTaskModal, setShowNewTaskModal] = useState(false);
  const [showEditTaskModal, setShowEditTaskModal] = useState<number | null>(null);
  const taskInputRef = useRef<HTMLInputElement>(null);
  const leaderboardInputRef = useRef<HTMLInputElement>(null);

  const handleNewTask = (e: React.KeyboardEvent | React.MouseEvent) => {
    if ('key' in e && e.key !== 'Enter') return;
    
    const taskName = taskInputRef.current?.value;
    if (taskName) {
      setTasks([...tasks, { id: Date.now(), name: taskName, difficulty: 0 }]);
      taskInputRef.current.value = '';
      setShowNewTaskModal(false);
    }
  };

  const handleNewLeaderboard = (e: React.KeyboardEvent | React.MouseEvent) => {
    if ('key' in e && e.key !== 'Enter') return;
    if (!isLoggedIn) {
      setShowAuthModal(true);
      return;
    }
    
    const leaderboardName = leaderboardInputRef.current?.value;
    if (leaderboardName) {
      setLeaderboards([...leaderboards, { 
        id: Date.now(), 
        name: leaderboardName,
        users: [{ id: Date.now(), username: "MyUsername", points: 0 }]
      }]);
      leaderboardInputRef.current.value = '';
      setSelectedLeaderboard(null);
    }
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(`${window.location.origin}/leaderboard/${selectedLeaderboard?.id}`);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 2000);
  };

  const handleAuth = (mode: 'login' | 'signup') => {
    // Implement actual authentication logic here
    setIsLoggedIn(true);
    setShowAuthModal(false);
  };

  const removeTask = (taskId: number) => {
    const taskElement = document.getElementById(`task-${taskId}`);
    if (taskElement) {
      taskElement.style.transform = 'rotate(10deg) translateX(100%)';
      taskElement.style.opacity = '0';
      setTimeout(() => {
        setTasks(tasks.filter(t => t.id !== taskId));
      }, 300);
    }
  };

  return (
    <div className="min-h-screen bg-white p-4">
      {/* Header */}
      <Card className="w-[60%] mx-auto h-16 mb-6 bg-[#efe1a7] rounded-xl shadow-[-12px_8px_4px_#00000040]">
        <CardContent className="flex items-center justify-center h-full">
          <h1 className="[font-family:'Jaro',Helvetica] text-4xl text-black text-center">
            COMP(L)ETE
          </h1>
        </CardContent>
      </Card>

      <div className="flex gap-6">
        {/* Leaderboards Section */}
        <div className="w-1/3">
          <Card className="bg-[#ffb6c1] rounded-xl shadow-[-12px_8px_4px_#00000040] mb-4 h-[calc(60vh+48px)]">
            <CardHeader>
              <CardTitle className="text-3xl [font-family:'Jaro',Helvetica]">
                LEADERBOARDS
              </CardTitle>
            </CardHeader>
            <CardContent className="max-h-[60vh] overflow-y-auto">
              {leaderboards.map((board) => (
                <Button
                  key={board.id}
                  className="w-full mb-2 text-left bg-[#e6e6fa] [font-family:'Jaro',Helvetica] text-black text-xl shadow-[0px_4px_4px_#00000040] hover:bg-[#d8d8f7]"
                  onClick={() => setSelectedLeaderboard(board)}
                >
                  {board.name}
                </Button>
              ))}
            </CardContent>
          </Card>

          <Button 
            className="w-full bg-[#eba68b] h-12 [font-family:'Jaro',Helvetica] text-2xl text-black shadow-[-12px_8px_4px_#00000040] hover:bg-[#e59577]"
            onClick={() => {
              if (!isLoggedIn) {
                setShowAuthModal(true);
                return;
              }
              setSelectedLeaderboard({ id: -1, name: '', users: [] });
            }}
          >
            Create Leaderboard
          </Button>
        </div>

        {/* Task Board Section */}
        <div className="w-2/3">
          <Card className="bg-[#abd1b0] rounded-xl shadow-[-12px_8px_4px_#00000040] mb-4 h-[calc(60vh+48px)]">
            <CardHeader>
              <CardTitle className="text-3xl [font-family:'Jaro',Helvetica]">
                TASK BOARD
              </CardTitle>
            </CardHeader>
            <CardContent className="h-[60vh] overflow-y-auto">
              <div className="grid grid-cols-4 gap-4">
                {tasks.map((task) => {
                  const [taskName, setTaskName] = useState(task.name);

                  return (
                    <div
                      id={`task-${task.id}`}
                      key={task.id}
                      className="relative"
                      onMouseEnter={(e) => {
                        e.stopPropagation();
                        e.currentTarget.querySelector('button')?.classList.remove('opacity-0');
                      }}
                      onMouseLeave={(e) => {
                        e.stopPropagation();
                        e.currentTarget.querySelector('button')?.classList.add('opacity-0');
                      }}
                    >
                      <Card onClick={() => removeTask(task.id)} className="bg-[#70db70] p-3 rotate-1 hover:rotate-3 transition-transform duration-200 min-h-[120px] relative shadow-lg border-t-8 border-[#7FDB7F] hover:bg-[#80e080] cursor-pointer" >
                        <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-6 h-2 bg-gray-400 rounded-sm"></div>
                        <div className="relative">
                          <span className="text-black [font-family:'Jaro',Helvetica] text-md block mb-2">{taskName}</span>
                          <Button onClick={() => setShowEditTaskModal(task.id)} className="absolute top-0 right-0 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-1 px-2 rounded opacity-0 transition-opacity duration-200">
                            Edit
                          </Button>
                        </div>
                        <div className="flex gap-1 mt-2">
                          {[...Array(5)].map((_, index) => (
                            <FaStar key={index} size={16} className={index < task.difficulty ? "text-yellow-500" : "text-gray-300"} />
                          ))}
                        </div>
                      </Card>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          <Button 
            className="w-full bg-[#b1d4f2] h-12 [font-family:'Jaro',Helvetica] text-2xl text-black shadow-[-12px_8px_4px_#00000040] hover:bg-[#9fc2e0]"
            onClick={() => setShowNewTaskModal(true)}
          >
            New Task
          </Button>
        </div>
      </div>

      {/* Auth Buttons */}
      <div className="absolute top-2 right-4 flex gap-4">
        <Button
          className="bg-[#b7b6b6] rounded-[10px] h-[26px] [font-family:'Jaro',Helvetica] w-[75px] ml-2"
          onClick={() => {
            setAuthMode('login');
            setShowAuthModal(true);
          }}
        >
          {isLoggedIn ? 'LOG OUT' : 'LOG IN'}
        </Button>
        <Button
          className="bg-[#b7b6b6] text-white h-[26px] p-0 rounded-[10px] [font-family:'Jaro',Helvetica] w-[75px] ml-2"
          onClick={() => {
            setAuthMode('signup');
            setShowAuthModal(true);
          }}
        >
          SIGN UP
        </Button>
      </div>

      {/* Modals */}
      <Dialog.Root open={!!selectedLeaderboard} onOpenChange={() => setSelectedLeaderboard(null)}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0" />
          <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-xl w-[400px]">
            <Dialog.Title className="text-2xl mb-4 [font-family:'Jaro',Helvetica]">
              {selectedLeaderboard?.id === -1 ? 'Create New Leaderboard' : selectedLeaderboard?.name}
            </Dialog.Title>
            {selectedLeaderboard?.id === -1 ? (
              <>
                <input
                  ref={leaderboardInputRef}
                  className="w-full p-2 border rounded mb-4"
                  placeholder="Leaderboard Name"
                  onKeyDown={handleNewLeaderboard}
                />
                <Button onClick={handleNewLeaderboard} className="[font-family:'Jaro',Helvetica]">Create</Button>
              </>
            ) : (
              <>
                <div className="max-h-[400px] overflow-y-auto mb-4">
                  {selectedLeaderboard?.users.map((user) => (
                    <div key={user.id} className="flex justify-between p-2 border-b [font-family:'Jaro',Helvetica]">
                      <span>{user.username}</span>
                      <span>{user.points}</span>
                    </div>
                  ))}
                </div>
                <div className="flex justify-between">
                  <Button onClick={handleCopyLink} className="[font-family:'Jaro',Helvetica]">Copy Link</Button>
                  <Button 
                    variant="destructive"
                    onClick={() => {
                      setLeaderboards(leaderboards.filter(b => b.id !== selectedLeaderboard?.id));
                      setSelectedLeaderboard(null);
                    }}
                    className="[font-family:'Jaro',Helvetica]"
                  >
                    Leave Leaderboard
                  </Button>
                </div>
              </>
            )}
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      <Dialog.Root open={showAuthModal} onOpenChange={setShowAuthModal}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-black/50" />
          <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-xl w-[400px]">
            <Dialog.Title className="text-2xl mb-4 [font-family:'Jaro',Helvetica]">
              {authMode === 'login' ? 'Log In' : 'Sign Up'}
            </Dialog.Title>
            {authMode === 'signup' && (
              <input
                className="w-full p-2 border rounded mb-4"
                placeholder="Username"
                type="text"
              />
            )}
            <input
              className="w-full p-2 border rounded mb-4"
              placeholder="Email"
              type="email"
            />
            <input
              className="w-full p-2 border rounded mb-4"
              placeholder="Password"
              type="password"
            />
            <Button onClick={() => handleAuth(authMode)} className="w-full [font-family:'Jaro',Helvetica] mb-4">
              {authMode === 'login' ? 'Log In' : 'Sign Up'}
            </Button>
            {authMode === 'login' && (
              <Button
                variant="ghost"
                onClick={() => setAuthMode('signup')}
                className="w-full text-sm text-gray-600 hover:text-gray-800"
              >
                Create account?
              </Button>
            )}
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {/* New Task Input Modal */}
      <Dialog.Root open={showNewTaskModal} onOpenChange={setShowNewTaskModal}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-black/50" />
          <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-xl w-[400px]">
            <Dialog.Title className="text-2xl mb-4 [font-family:'Jaro',Helvetica]">New Task</Dialog.Title>
            <input
              ref={taskInputRef}
              className="w-full p-2 border rounded mb-4"
              placeholder="Task Name"
              onKeyDown={handleNewTask}
            />
            <Button onClick={handleNewTask} className="w-full [font-family:'Jaro',Helvetica]">Create Task</Button>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {/* Toast for Copy Link */}
      <Toast.Provider>
        <Toast.Root
          open={showToast}
          onOpenChange={setShowToast}
          className="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-lg [font-family:'Jaro',Helvetica]"
        >
          Link copied!
        </Toast.Root>
      </Toast.Provider>

      {/* Edit Task Input Modal */}
      <Dialog.Root open={showEditTaskModal !== null} onOpenChange={() => setShowEditTaskModal(null)}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-black/50" />
          <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-xl w-[400px]">
            <Dialog.Title className="text-2xl mb-4 [font-family:'Jaro',Helvetica]">Edit Task</Dialog.Title>
            {tasks.find(t => t.id === showEditTaskModal) && (
              <>
                {(() => {
                  const [taskName, setTaskName] = useState(tasks.find(t => t.id === showEditTaskModal)?.name || '');
                  return (
                    <>
                      <input
                        className="w-full p-2 border rounded mb-4"
                        placeholder="Task Name"
                        value={taskName}
                        onChange={(e) => {
                          setTaskName(e.target.value);
                        }}
                      />
                      <Button onClick={() => {
                        setTasks(prevTasks =>
                          prevTasks.map(t =>
                            t.id === showEditTaskModal ? { ...t, name: taskName } : t
                          )
                        );
                        setShowEditTaskModal(null);
                      }} className="w-full [font-family:'Jaro',Helvetica]">Update Task</Button>
                    </>
                  );
                })()}
              </>
            )}
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </div>
  );
};