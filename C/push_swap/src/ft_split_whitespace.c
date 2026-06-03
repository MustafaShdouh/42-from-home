/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split_whitespace.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/13 19:51:32 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/13 20:43:46 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include <stdlib.h>

static void	*free_array(char **str, int count)
{
	while (count > 0)
	{
		count--;
		free(str[count]);
	}
	free(str);
	return (NULL);
}

static int	is_whitespace(char c)
{
	return (c == ' ' || c == '\t' || c == '\n' || c == '\v'
		|| c == '\f' || c == '\r');
}

static int	count_words(char *str)
{
	int	count;
	int	i;

	count = 0;
	i = 0;
	while (str[i])
	{
		while (str[i] && is_whitespace(str[i]))
			i++;
		if (str[i])
			count++;
		while (str[i] && !is_whitespace(str[i]))
			i++;
	}
	return (count);
}

static char	*get_next_word(char *str)
{
	char	*word;
	int		len;
	int		i;

	len = 0;
	while (str[len] && !is_whitespace(str[len]))
		len++;
	word = (char *)malloc(sizeof(char) * (len + 1));
	if (!word)
		return (NULL);
	i = 0;
	while (i < len)
	{
		word[i] = str[i];
		i++;
	}
	word[i] = '\0';
	return (word);
}

char	**ft_split_whitespace(char *str)
{
	char	**result;
	int		i;
	int		words;

	words = count_words(str);
	result = (char **)malloc(sizeof(char *) * (words + 1));
	if (!result)
		return (NULL);
	i = 0;
	while (*str)
	{
		while (*str && is_whitespace(*str))
			str++;
		if (*str)
		{
			result[i] = get_next_word(str);
			if (!result[i])
				return (free_array(result, i));
			i++;
			while (*str && !is_whitespace(*str))
				str++;
		}
	}
	result[i] = NULL;
	return (result);
}
