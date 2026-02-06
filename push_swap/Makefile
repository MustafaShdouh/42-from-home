# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/04 19:39:10 by mel-shdo          #+#    #+#              #
#    Updated: 2026/02/06 21:00:15 by mel-shdo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME		= push_swap
CC			= cc
CFLAGS		= -Wall -Werror -Wextra

LIBFT_DIR	= ./libft
LIBFT		= $(LIBFT_DIR)/libft.a
INCLUDES	= -I $(LIBFT_DIR)

SRC_DIR     = src
STACK_DIR   = src/stack
OPS_DIR     = src/ops
STRAT_DIR   = src/strategies

SRCS        = $(SRC_DIR)/push_swap.c \
              $(SRC_DIR)/parsing.c \
              $(SRC_DIR)/metrics.c \
              $(SRC_DIR)/errors.c \
              $(SRC_DIR)/utils_lib.c \
              $(STACK_DIR)/stack_init.c \
              $(STACK_DIR)/stack_utils.c \
              $(OPS_DIR)/push.c \
              $(OPS_DIR)/swap.c \
              $(OPS_DIR)/rotate.c \
              $(OPS_DIR)/reverse_rotate.c \
              $(STRAT_DIR)/sort_simple.c \
              $(STRAT_DIR)/sort_medium.c \
              $(STRAT_DIR)/sort_complex.c \
              $(STRAT_DIR)/sort_adaptive.c

OBJS	= $(SRCS:.c=.o)

all: $(NAME)

$(LIBFT):
		@make -C $(LIBFT_DIR)

$(NAME): $(LIBFT) $(OBJS)
		$(CC) $(CFLAGS) $(OBJS) $(LIBFT) -o $(NAME)

%.o : %.c
		$(CC) $(CFLAGS) -c $< -o $@

clean:
		rm -f $(OBJS)
		@make -C $(LIBFT_DIR) fclean

fclean: clean
		rm -f $(NAME)
		@make -C $(LIBFT_DIR) fclean

re: fclean all

.PHONY: all clean fclean re