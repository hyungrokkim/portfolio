#include <vector>
#include <utility>
#include <algorithm>
#include <iostream>
#include <string>
#include <istream>
#include <ostream>
#include <cassert>
#include <stdexcept>
#include <climits>
#include <ctime>

#define FOR_BOARD(x, y) for(int x=0; x<board::size; ++x)\
                          for(int y=0; y<board::size; ++y)
#define FOR_DIRECTION(x, y) for(int x=-1; x<2; ++x)\
                              for(int y=-1; y<2; ++y)\
                                if(x==0&&y==0); else

using std::vector;
using std::pair;
using std::out_of_range;
using std::cin;
using std::cout;
using std::cerr;
using std::endl;
using std::time_t;
using std::time;
using std::difftime;
class game {
public:
  class board {
  public:
    enum state {empty, white, black};
    static state enemy(state s) {
      switch(s) {
      case white: return black;
      case black: return white;
      default: return empty;
      }
    }
    static int const size=8;
    // accessors
    state& operator()(int x, int y) {
      if(!valid_index(x) || !valid_index(y))
        throw out_of_range("invalid indices");
      return pieces[x][y];
    }
    state const& operator()(int x, int y) const {
      if(!valid_index(x) || !valid_index(y))
        throw out_of_range("invalid indices");
      return pieces[x][y];
    }
    pair<bool, board> play(int x, int y) const;
    static board initial() {
      board b;
      b.pieces=vector<vector<state> >(8, vector<state>(8, empty));
      b(3,3)=b(4,4)=white;
      b(4,3)=b(3,4)=black;
      return b;
    }
    board() { *this=initial(); }
  private:
    static bool valid_index(int i) { return i>=0 && i<board::size; }
    vector<vector<state> > pieces;
    state turn;
  };
  board const& current() const { return current_node->current; }
  vector<game*> const& next() const;
  pair<int, int> const& last_move() const { return current_node->move; }
  void move(int, int);
  bool can_move(int, int);
  int eval() const;
  game(): current_node(new node(board::initial(), pair<int,int>(-1,-1))) {}
private:
  struct node {
    board const current;
    mutable vector<game*>* next;
    pair<int, int> const move;
    int const eval;
    node(board const& b, pair<int,int> const& m);
  }* current_node;
  static void remove(node* n) {
    if(n->next) {
      for(vector<game*>::iterator i=n->next->begin(); i!=n->next->end(); ++i) {
        remove((*i)->current_node);
        delete *i;
      }
      delete n->next;
    }
    delete n;
  }
};


typedef game::board board;

vector<game*> const& game::next() const {
  if(!(current_node->next)) {
    current_node->next=new vector<game*>();
    FOR_BOARD(i, j) {
      pair<bool, board> const p=current_node->current.play(i, j);
      if(p.first) {
        game* g=new game;
        g->current_node=new game::node(p.second, pair<int,int>(i,j));
        current_node->next->push_back(g);
      }
    }
  }
  return *(current_node->next);
}

void game::move(int x, int y) {
  game::node* n=NULL;
  for(vector<game*>::const_iterator i=next().begin(); i!=next().end(); ++i) {
    if((*i)->current_node->move==pair<int,int>(x, y)) n=(*i)->current_node;
    else remove((*i)->current_node);
  }
  delete current_node->next;
  delete current_node;
  current_node=n;
}
bool game::can_move(int x, int y) {
  for(vector<game*>::const_iterator i=next().begin(); i!=next().end(); ++i)
    if((*i)->current_node->move==pair<int,int>(x, y)) return true;
  return false;
}

inline pair<bool, board> game::board::play(int x, int y) const {
  game::board b(*this);
  b.turn=game::board::enemy(turn);
  bool valid=false;
  if(b(x, y)==empty)
    FOR_DIRECTION(i, j)
      for(int xx=x+i, yy=y+j; valid_index(xx) && valid_index(yy); xx+=i, yy+=j)
        if(b(xx, yy)==empty) break;
        else if(b(xx, yy)==turn) {
          if(xx!=x+i||yy!=y+j) {
            for(int xxx=x+i, yyy=y+j; xxx!=xx || yyy!=yy; xxx+=i, yyy+=j)
              b(xxx, yyy) = turn;
            valid=true;
          }
          break;
        }
  return pair<bool, board>(valid, b);
}

inline int game::eval() const {
  return current_node->eval;
}


int evaluate(board const& b) {
  int i=0;
  for(int x=1; x<board::size-1; ++x) for(int y=1; y<board::size-1; ++y) {
    if(b(x, y)==board::white) i++;
    if(b(x, y)==board::black) i--;
  }
  int const side_advantage = 5;
  for(int x=1; x<board::size-1; ++x) {
    if(b(x, 0)==board::white) i+=side_advantage;
    if(b(x, 0)==board::black) i-=side_advantage;
    if(b(x, board::size-1)==board::white) i+=side_advantage;
    if(b(x, board::size-1)==board::black) i-=side_advantage;
    if(b(0, x)==board::white) i+=side_advantage;
    if(b(0, x)==board::black) i-=side_advantage;
    if(b(board::size-1, x)==board::white) i+=side_advantage;
    if(b(board::size-1, x)==board::black) i-=side_advantage;
  }
  int const corner_advantage = 50;
  if(b(0, 0)==board::white) i+=corner_advantage;
  if(b(0, 0)==board::black) i-=corner_advantage;
  if(b(0, board::size-1)==board::white) i+=corner_advantage;
  if(b(0, board::size-1)==board::black) i-=corner_advantage;
  if(b(board::size-1, 0)==board::white) i+=corner_advantage;
  if(b(board::size-1, 0)==board::black) i-=corner_advantage;
  if(b(board::size-1, board::size-1)==board::white) i+=corner_advantage;
  if(b(board::size-1, board::size-1)==board::black) i-=corner_advantage;
  return i;
}


game::node::node(board const& b, pair<int,int> const& m): current(b), next(NULL), move(m),
    eval(evaluate(b)) {}

int search(game const& g, int depth, int alpha, int beta) {
  if(g.next().empty() || !depth) return g.eval();
  for(std::vector<game*>::const_iterator i=g.next().begin(); i!=g.next().end(); ++i) {
    alpha = std::max(alpha, -search(**i, depth-1, -beta, -alpha));
    if(alpha>=beta) return alpha;
  }
  return alpha;
}

std::pair<int, int> best(game const& g) {/*
  int i=0;
  FOR_BOARD(x, y) {
    if(b.play(x, y).first) ++i;
  }*/
  int const depth = 8; // no of recursions

  if(g.next().empty() || !depth) return std::pair<int, int>(-1, -1);
  pair<int, int> p = std::pair<int, int>(-1, -1); // pass
  int a = INT_MIN;
  for(std::vector<game*>::const_iterator i=g.next().begin(); i!=g.next().end(); ++i) {
    int s = search(**i, depth, INT_MIN, INT_MAX);
    //std::cerr<<"pair ("<<i->first+1<<", "<<i->second+1<<") is "<<s<<std::endl;
    if(s>a) {
      p=(*i)->last_move();
      a=s;
    }
  }
  return p;
}



game::board::state winner(game::board const& b) {
  int i=0;
  FOR_BOARD(x, y)
    switch(b(x, y)) {
      case game::board::white: i++; break;
      case game::board::black: i--; break;
      default: break;
    }
  return i>0 ? game::board::white : i<0 ? game::board::black : game::board::empty;
}

template <typename Elem, typename Tr>
std::basic_ostream<Elem, Tr>& operator<<(std::basic_ostream<Elem, Tr>& s, game::board const& b) {
  for(int i=0; i<game::board::size; ++i) {
    for(int j=0; j<game::board::size; ++j) {
      switch(b(i, j)) {
      case board::empty:
        s<<std::basic_string<Elem, Tr>(1,'_');
        break;
      case board::white:
        s<<std::basic_string<Elem, Tr>(1,'O');
        break;
      case board::black:
        s<<std::basic_string<Elem, Tr>(1,'#');
        break;
      }
      s<<std::basic_string<Elem, Tr>(1,' ');
    }
    s<<std::endl;
  }
  return s;
}

int main() {
  cout<<"Welcome, stranger, to Messrs Kim, Kweon & Lee's "
             "fantasmagorical hall of Othello!\n"
             "Darest thou challenge me, the AI of AIs?\n";
  cout<<"Remember, thou art dark!\n";
  
  game g;
  while(true) {
    cout<<g.current();
    cout<<"Challenger, move if thou darest: ";
    int x, y;
    cin>>x>>y;
    
    if(g.can_move(x-1, y-1)) g.move(x-1, y-1); else {
       cout<<"Fool! Thy moves are foetid!\n";
       continue;
    }
    if(g.next().empty()) break;
    cout<<g.current();
    time_t t1 = time(NULL);
    pair<int, int> n(best(g));
    cerr<<"It took "<<difftime(time(NULL), t1)<<" s.\n";
    cout<<"Lo and behold! For I shall play at ("<<n.first+1<<", "<<n.second+1<<")!\n";
    assert(g.can_move(n.first, n.second));
    g.move(n.first, n.second);
    std::cout<<"Current evaluation: "<<g.eval()<<std::endl;
    if(g.next().empty()) break;
  }
  std::cout<<g.current();
  switch(winner(g.current())) {
    case game::board::black:
      std::cout<<"Curses be damned! Thou hast won, but not for long...\n";
      break;
    case game::board::white:
      std::cout<<"Alleluia! I have bested thee!\n";
      break;
    case game::board::empty:
      std::cout<<"Alas, 'tis a tie, but not for long...\n";
  }
}
