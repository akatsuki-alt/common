from common.api.server_api import User
from dataclasses import dataclass
from typing import Type, Callable

class EventHandler:
    
    def __init__(self) -> None:
        self.handlers = {}

    def add_handler(self, function: Callable, event: Type=None):
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(function)
    
    def remove_handler(self, function: Callable, event: Type=None):
        if event not in self.handlers or function not in self.handlers[event]:
            return
        self.handlers[event].remove(function)
    
    def trigger(self, event: object):
        for handler in self.handlers[None] if None in self.handlers else []:
            handler(event)
        if type(event) not in self.handlers:
            return
        for handler in self.handlers[type(event)]:
            handler(event)

@dataclass
class LeaderboardUpdateEvent:
    server: str
    type: str
    users_updated: int

    def __repr__(self) -> str:
        return f"Updated leaderboard for server {self.server}! (Total users updated: {self.users_updated})"

@dataclass
class NewUserDiscoveredEvent:
    user: User
    
    def __repr__(self) -> str:
        return f"New user discovered!\nServer: {self.user.server}\nUsername: {self.user.username}"

@dataclass
class BannedUserEvent:
    user_id: int
    server: str
    user: User | None
    
    def __repr__(self) -> str:
        username = self.user.username if self.user else "No username recorded."
        return f"New banned user discovered! {username} ({self.user_id}, {self.server})"